/**
 * Hockey-themed Loading Animations
 * For Namibia Hockey Union Application
 */

// Global loader instance
let loader = {
    container: null,
    isVisible: false,
    messages: [
        "Passing the puck...",
        "Taking a slap shot...",
        "Skating to goal...",
        "Checking the play...",
        "Saving the shot...",
        "Crossing the blue line...",
        "Setting up the power play..."
    ],
    
    // Initialize the loader
    init: function() {
        // Create loader container if it doesn't exist
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'loader-container';
            
            // Create hockey-themed loader elements
            let loaderHTML = `
                <div class="hockey-loader">
                    <div class="hockey-puck"></div>
                    <div class="hockey-stick"></div>
                    <div class="ice-rink"></div>
                    <div class="goal-net"></div>
                    <div class="loading-text">Loading...</div>
                </div>
            `;
            
            // Create page transition elements
            let transitionHTML = `
                <div class="page-transition">
                    <div class="hockey-line"></div>
                    <div class="hockey-line"></div>
                    <div class="hockey-line"></div>
                    <div class="hockey-line"></div>
                    <div class="hockey-line"></div>
                </div>
            `;
            
            this.container.innerHTML = loaderHTML;
            document.body.appendChild(this.container);
            document.body.insertAdjacentHTML('beforeend', transitionHTML);
            
            // Store references
            this.pageTransitionElement = document.querySelector('.page-transition');
            this.loadingText = document.querySelector('.loading-text');
        }
    },
    
    // Show the loader with optional custom message
    show: function(message) {
        this.init();
        
        // Set loading message
        if (message) {
            this.loadingText.textContent = message;
        } else {
            // Set random hockey-themed message
            const randomIndex = Math.floor(Math.random() * this.messages.length);
            this.loadingText.textContent = this.messages[randomIndex];
        }
        
        // Show loader
        this.container.classList.add('show');
        this.isVisible = true;
        
        // Prevent scrolling on body
        document.body.style.overflow = 'hidden';
    },
    
    // Hide the loader
    hide: function() {
        if (this.isVisible) {
            this.container.classList.remove('show');
            this.isVisible = false;
            
            // Restore scrolling
            document.body.style.overflow = '';
        }
    },
    
    // Perform a page transition
    pageTransition: function(callback) {
        this.init();
        
        // Show transition
        this.pageTransitionElement.classList.add('show');
        
        // After animation completes
        setTimeout(() => {
            if (callback && typeof callback === 'function') {
                callback();
            }
            
            // Hide transition with exit animation
            this.pageTransitionElement.classList.remove('show');
            this.pageTransitionElement.classList.add('hide');
            
            // Reset after exit animation
            setTimeout(() => {
                this.pageTransitionElement.classList.remove('hide');
            }, 500);
        }, 1000);
    }
};

// Add event listeners to automatically show loader on page navigation
document.addEventListener('DOMContentLoaded', function() {
    // Add loading animation to all form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            loader.show();
        });
    });
    
    // Add loading animation to navigation links
    document.querySelectorAll('a:not([target="_blank"])').forEach(link => {
        link.addEventListener('click', function(e) {
            // Ignore links with # that are for JavaScript functionality
            if (this.getAttribute('href').startsWith('#')) {
                return;
            }
            
            e.preventDefault();
            const targetUrl = this.getAttribute('href');
            
            loader.pageTransition(() => {
                window.location.href = targetUrl;
            });
        });
    });
    
    // Add AJAX request interceptor for fetch API
    const originalFetch = window.fetch;
    window.fetch = function() {
        loader.show();
        return originalFetch.apply(this, arguments)
            .then(response => {
                loader.hide();
                return response;
            })
            .catch(error => {
                loader.hide();
                throw error;
            });
    };
    
    // Hide loader when page is fully loaded
    window.addEventListener('load', function() {
        setTimeout(() => {
            loader.hide();
        }, 500);
    });
});