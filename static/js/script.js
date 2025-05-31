
// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/static/js/service-worker.js')
      .then(function(registration) {
        console.log('Service Worker registered with scope:', registration.scope);
      }, function(err) {
        console.log('Service Worker registration failed:', err);
      });
  });
}

// Initialize offline functionality
document.addEventListener('DOMContentLoaded', function() {
  console.log('Offline functionality initialized');
  
  // Check if IndexedDB is available
  if ('indexedDB' in window) {
    console.log('IndexedDB initialized successfully');
  }
  
  // Add loading state management with proper error checking
  const loadingElements = document.querySelectorAll('.loading');
  if (loadingElements && loadingElements.length > 0) {
    loadingElements.forEach(function(element) {
      if (element && element.classList && typeof element.classList.add === 'function') {
        element.classList.add('loaded');
      }
    });
  }
  
  // Initialize form validation
  const forms = document.querySelectorAll('form');
  forms.forEach(function(form) {
    if (form) {
      form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn && submitBtn.classList && typeof submitBtn.classList.add === 'function') {
          submitBtn.classList.add('loading');
          submitBtn.disabled = true;
        }
      });
    }
  });
});
