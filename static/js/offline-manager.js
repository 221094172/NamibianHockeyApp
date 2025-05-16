/**
 * Offline Functionality Manager
 * Provides offline capabilities for the Namibia Hockey Union App
 */

const offlineManager = {
    // Configuration
    config: {
        cacheVersion: 'nhu-cache-v1',
        offlineMessage: 'You are currently offline. Some features may be limited.',
        syncMessage: 'Syncing data...',
        syncCompleteMessage: 'Data synced successfully!',
        dataStores: ['teams', 'players', 'events', 'notifications']
    },
    
    // Initialize offline functionality
    init: function() {
        // Check if the browser supports Service Worker and IndexedDB
        if ('serviceWorker' in navigator && 'indexedDB' in window) {
            // Register service worker for caching static assets
            this.registerServiceWorker();
            
            // Initialize IndexedDB for offline data storage
            this.initIndexedDB();
            
            // Set up online/offline event listeners
            this.setupConnectionListeners();
            
            // Initial connection check
            this.checkConnection();
            
            // Set up form submission interceptors for offline handling
            this.setupFormInterceptors();
            
            console.log('Offline functionality initialized');
        } else {
            console.warn('Browser does not support offline functionality');
        }
    },
    
    // Register service worker
    registerServiceWorker: function() {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then(registration => {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(error => {
                console.error('Service Worker registration failed:', error);
            });
    },
    
    // Initialize IndexedDB
    initIndexedDB: function() {
        const request = indexedDB.open('NamibiaHockeyDB', 1);
        
        request.onerror = function(event) {
            console.error('IndexedDB error:', event.target.error);
        };
        
        request.onupgradeneeded = function(event) {
            const db = event.target.result;
            
            // Create object stores for each data type
            offlineManager.config.dataStores.forEach(storeName => {
                if (!db.objectStoreNames.contains(storeName)) {
                    db.createObjectStore(storeName, { keyPath: 'id', autoIncrement: true });
                    console.log(`Created object store: ${storeName}`);
                }
            });
            
            // Create a special store for pending operations when offline
            if (!db.objectStoreNames.contains('pendingOperations')) {
                db.createObjectStore('pendingOperations', { keyPath: 'timestamp' });
                console.log('Created pendingOperations store');
            }
        };
        
        request.onsuccess = function(event) {
            offlineManager.db = event.target.result;
            console.log('IndexedDB initialized successfully');
            
            // If online, sync any pending operations
            if (navigator.onLine) {
                offlineManager.syncPendingOperations();
            }
        };
    },
    
    // Set up online/offline event listeners
    setupConnectionListeners: function() {
        window.addEventListener('online', () => {
            this.checkConnection();
            this.syncPendingOperations();
        });
        
        window.addEventListener('offline', () => {
            this.checkConnection();
        });
    },
    
    // Check connection status and update UI
    checkConnection: function() {
        const connectionStatus = document.getElementById('connection-status');
        
        if (!connectionStatus) {
            // Create connection status element if it doesn't exist
            const statusEl = document.createElement('div');
            statusEl.id = 'connection-status';
            statusEl.className = 'connection-status';
            document.body.appendChild(statusEl);
        }
        
        const statusEl = document.getElementById('connection-status');
        
        if (navigator.onLine) {
            statusEl.textContent = '';
            statusEl.classList.remove('offline');
            statusEl.classList.add('online');
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 3000);
        } else {
            statusEl.textContent = this.config.offlineMessage;
            statusEl.classList.remove('online');
            statusEl.classList.add('offline');
            statusEl.style.display = 'block';
        }
    },
    
    // Setup form submission interceptors
    setupFormInterceptors: function() {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(e) {
                // If offline, prevent default submission and store it
                if (!navigator.onLine) {
                    e.preventDefault();
                    
                    const formData = new FormData(this);
                    const formObject = {};
                    
                    formData.forEach((value, key) => {
                        formObject[key] = value;
                    });
                    
                    // Store the operation for later
                    offlineManager.storeOperation({
                        type: 'form',
                        method: this.method,
                        action: this.action,
                        data: formObject,
                        timestamp: Date.now()
                    });
                    
                    // Show feedback to user
                    alert('You are offline. Your changes will be saved and synced when you are back online.');
                    
                    // If this is a create/edit form, update the UI optimistically
                    offlineManager.updateUIOptimistically(formObject);
                }
            });
        });
    },
    
    // Store an operation for later when online
    storeOperation: function(operation) {
        if (!this.db) {
            console.error('Database not initialized');
            return;
        }
        
        const transaction = this.db.transaction(['pendingOperations'], 'readwrite');
        const store = transaction.objectStore('pendingOperations');
        
        store.add(operation);
        
        transaction.oncomplete = function() {
            console.log('Operation stored for later sync:', operation);
        };
        
        transaction.onerror = function(event) {
            console.error('Error storing operation:', event.target.error);
        };
    },
    
    // Sync pending operations when back online
    syncPendingOperations: function() {
        if (!this.db || !navigator.onLine) {
            return;
        }
        
        // Show syncing message
        this.showMessage(this.config.syncMessage);
        
        const transaction = this.db.transaction(['pendingOperations'], 'readwrite');
        const store = transaction.objectStore('pendingOperations');
        const request = store.getAll();
        
        request.onsuccess = function(event) {
            const operations = event.target.result;
            
            if (operations.length === 0) {
                offlineManager.hideMessage();
                return;
            }
            
            // Process each operation in order
            operations.sort((a, b) => a.timestamp - b.timestamp);
            
            let operationsCompleted = 0;
            
            operations.forEach(operation => {
                // Submit the form data via fetch
                if (operation.type === 'form') {
                    fetch(operation.action, {
                        method: operation.method,
                        body: new URLSearchParams(operation.data),
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            // Remove from pending operations
                            const delTransaction = offlineManager.db.transaction(['pendingOperations'], 'readwrite');
                            const delStore = delTransaction.objectStore('pendingOperations');
                            delStore.delete(operation.timestamp);
                            
                            operationsCompleted++;
                            if (operationsCompleted === operations.length) {
                                offlineManager.showMessage(offlineManager.config.syncCompleteMessage);
                                setTimeout(() => {
                                    offlineManager.hideMessage();
                                }, 3000);
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error syncing operation:', error);
                    });
                }
            });
        };
        
        request.onerror = function(event) {
            console.error('Error retrieving pending operations:', event.target.error);
            offlineManager.hideMessage();
        };
    },
    
    // Show a message to the user
    showMessage: function(message) {
        const messageEl = document.getElementById('sync-message') || document.createElement('div');
        messageEl.id = 'sync-message';
        messageEl.className = 'sync-message';
        messageEl.textContent = message;
        
        if (!document.getElementById('sync-message')) {
            document.body.appendChild(messageEl);
        }
        
        messageEl.style.display = 'block';
    },
    
    // Hide the message
    hideMessage: function() {
        const messageEl = document.getElementById('sync-message');
        if (messageEl) {
            messageEl.style.display = 'none';
        }
    },
    
    // Update UI optimistically when offline
    updateUIOptimistically: function(formData) {
        // Determine what kind of form this is
        if (formData.hasOwnProperty('name') && formData.hasOwnProperty('division')) {
            // Likely a team form
            this.addOptimisticTeam(formData);
        } else if (formData.hasOwnProperty('first_name') && formData.hasOwnProperty('last_name')) {
            // Likely a player form
            this.addOptimisticPlayer(formData);
        } else if (formData.hasOwnProperty('title') && formData.hasOwnProperty('content')) {
            // Likely a notification form
            this.addOptimisticNotification(formData);
        }
    },
    
    // Add a team optimistically to the UI
    addOptimisticTeam: function(teamData) {
        // Check if we're on the team list page
        const teamsList = document.querySelector('.teams-list');
        if (!teamsList) return;
        
        // Create a new team card with an "Offline" badge
        const teamCard = document.createElement('div');
        teamCard.className = 'col-md-4 mb-4';
        teamCard.innerHTML = `
            <div class="card h-100 team-card offline-item">
                <div class="card-body">
                    <h5 class="card-title">${teamData.name} <span class="badge bg-warning">Offline</span></h5>
                    <p class="card-text">Division: ${teamData.division}</p>
                    <p class="card-text">Founded: ${teamData.founded_year || 'N/A'}</p>
                </div>
                <div class="card-footer">
                    <small class="text-muted">Pending sync</small>
                </div>
            </div>
        `;
        
        teamsList.appendChild(teamCard);
    },
    
    // Add a player optimistically to the UI
    addOptimisticPlayer: function(playerData) {
        // Check if we're on the player list page
        const playersList = document.querySelector('.players-list');
        if (!playersList) return;
        
        // Create a new player card with an "Offline" badge
        const playerCard = document.createElement('div');
        playerCard.className = 'col-md-4 mb-4';
        playerCard.innerHTML = `
            <div class="card h-100 player-card offline-item">
                <div class="card-body">
                    <h5 class="card-title">${playerData.first_name} ${playerData.last_name} <span class="badge bg-warning">Offline</span></h5>
                    <p class="card-text">Position: ${playerData.position}</p>
                    <p class="card-text">Jersey: ${playerData.jersey_number || 'N/A'}</p>
                </div>
                <div class="card-footer">
                    <small class="text-muted">Pending sync</small>
                </div>
            </div>
        `;
        
        playersList.appendChild(playerCard);
    },
    
    // Add a notification optimistically to the UI
    addOptimisticNotification: function(notificationData) {
        // Check if we're on the notifications page
        const notificationsList = document.querySelector('.notifications-list');
        if (!notificationsList) return;
        
        // Create a new notification with an "Offline" badge
        const notificationItem = document.createElement('div');
        notificationItem.className = 'card mb-3 notification-card offline-item';
        notificationItem.innerHTML = `
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">${notificationData.title} <span class="badge bg-warning">Offline</span></h5>
                <small class="text-muted">Just now</small>
            </div>
            <div class="card-body">
                <p class="card-text">${notificationData.content}</p>
            </div>
            <div class="card-footer">
                <small class="text-muted">Pending sync</small>
            </div>
        `;
        
        notificationsList.prepend(notificationItem);
    },
    
    // Store data locally
    storeData: function(storeName, data) {
        if (!this.db) {
            console.error('Database not initialized');
            return Promise.reject('Database not initialized');
        }
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.add(data);
            
            request.onsuccess = function() {
                resolve(request.result);
            };
            
            request.onerror = function(event) {
                reject(event.target.error);
            };
        });
    },
    
    // Retrieve data locally
    getData: function(storeName, id) {
        if (!this.db) {
            console.error('Database not initialized');
            return Promise.reject('Database not initialized');
        }
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = id ? store.get(id) : store.getAll();
            
            request.onsuccess = function() {
                resolve(request.result);
            };
            
            request.onerror = function(event) {
                reject(event.target.error);
            };
        });
    }
};

// Initialize the offline manager when the page loads
document.addEventListener('DOMContentLoaded', function() {
    offlineManager.init();
});