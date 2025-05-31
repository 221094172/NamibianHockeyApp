class OfflineManager {
  constructor() {
    this.isOnline = navigator.onLine;
    this.init();
  }

  init() {
    // Listen for online/offline events
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());

    // Initialize UI state
    this.updateUI();
  }

  handleOnline() {
    this.isOnline = true;
    console.log('App is online');
    this.updateUI();
    this.syncPendingData();
  }

  handleOffline() {
    this.isOnline = false;
    console.log('App is offline');
    this.updateUI();
  }

  updateUI() {
    const offlineIndicator = document.querySelector('.offline-indicator');
    const onlineIndicator = document.querySelector('.online-indicator');

    if (this.isOnline) {
      if (offlineIndicator && offlineIndicator.classList) {
        offlineIndicator.classList.add('hidden');
      }
      if (onlineIndicator && onlineIndicator.classList) {
        onlineIndicator.classList.remove('hidden');
      }
    } else {
      if (offlineIndicator && offlineIndicator.classList) {
        offlineIndicator.classList.remove('hidden');
      }
      if (onlineIndicator && onlineIndicator.classList) {
        onlineIndicator.classList.add('hidden');
      }
    }
  }

  syncPendingData() {
    // Implement data synchronization when back online
    console.log('Syncing pending data...');
  }
}

// Initialize offline manager
document.addEventListener('DOMContentLoaded', function() {
  try {
    window.offlineManager = new OfflineManager();
  } catch (error) {
    console.error('Failed to initialize offline manager:', error);
  }
});