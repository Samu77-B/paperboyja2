/**
 * Navigation Component Loader
 * Loads the modern navigation bar component and initializes functionality
 */

(function() {
  'use strict';
  
  // Load the navigation component
  function loadNavigation() {
    fetch('/nav-component.html')
      .then(response => response.text())
      .then(html => {
        // Insert nav at the beginning of body
        const navPlaceholder = document.getElementById('nav-placeholder');
        if (navPlaceholder) {
          navPlaceholder.innerHTML = html;
        } else {
          // Fallback: insert at beginning of body
          document.body.insertAdjacentHTML('afterbegin', html);
        }
        
        // Initialize navigation after loading
        initializeNavigation();
        
        // Set active menu item based on current page
        setActiveMenuItem();
        
        // Initialize Ecwid cart if available
        initializeEcwidCart();
      })
      .catch(error => {
        console.error('Error loading navigation:', error);
      });
  }
  
  // Initialize Ecwid cart widget
  function initializeEcwidCart() {
    // Wait for Ecwid to be available
    var checkEcwid = setInterval(function() {
      if (typeof Ecwid !== 'undefined' && Ecwid.init) {
        clearInterval(checkEcwid);
        // Ecwid should already be initialized, just ensure it's aware of the cart widget
        if (typeof Ecwid.refreshConfig === 'function') {
          Ecwid.refreshConfig();
        }
      }
    }, 100);
    
    // Stop checking after 5 seconds
    setTimeout(function() {
      clearInterval(checkEcwid);
    }, 5000);
  }
  
  // Initialize navigation functionality
  function initializeNavigation() {
    // Search overlay toggle
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    
    if (searchToggle) {
      searchToggle.addEventListener('click', function() {
        searchOverlay.classList.add('active');
      });
    }
    
    if (searchClose) {
      searchClose.addEventListener('click', function() {
        searchOverlay.classList.remove('active');
      });
    }
    
    if (searchOverlay) {
      searchOverlay.addEventListener('click', function(e) {
        if (e.target === searchOverlay) {
          searchOverlay.classList.remove('active');
        }
      });
    }
    
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuToggle && mobileMenu) {
      mobileMenuToggle.addEventListener('click', function() {
        mobileMenuToggle.classList.toggle('active');
        mobileMenu.classList.toggle('active');
      });
    }
    
    // Mobile dropdown toggle
    const mobileDropdownTriggers = document.querySelectorAll('.mobile-dropdown-trigger');
    mobileDropdownTriggers.forEach(function(trigger) {
      trigger.addEventListener('click', function() {
        const submenu = this.nextElementSibling;
        if (submenu) {
          submenu.classList.toggle('active');
        }
      });
    });
    
    // Improved mega menu hover behavior with delay
    const navDropdown = document.querySelector('.nav-item-dropdown');
    const megaMenu = document.querySelector('.mega-menu');
    let closeTimeout;
    
    if (navDropdown && megaMenu) {
      // Add active class on hover
      navDropdown.addEventListener('mouseenter', function() {
        clearTimeout(closeTimeout);
        megaMenu.classList.add('mega-menu-active');
      });
      
      // Keep menu open when hovering over it
      megaMenu.addEventListener('mouseenter', function() {
        clearTimeout(closeTimeout);
        megaMenu.classList.add('mega-menu-active');
      });
      
      // Delay closing when mouse leaves
      navDropdown.addEventListener('mouseleave', function() {
        closeTimeout = setTimeout(function() {
          megaMenu.classList.remove('mega-menu-active');
        }, 300);
      });
      
      megaMenu.addEventListener('mouseleave', function() {
        closeTimeout = setTimeout(function() {
          megaMenu.classList.remove('mega-menu-active');
        }, 300);
      });
    }
    
    // Initialize Ecwid search in nav overlay
    if (typeof xSearch !== 'undefined') {
      xSearch("id=my-search-64309912");
    }
  }
  
  // Set active menu item based on current page
  function setActiveMenuItem() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item-modern[href], .mobile-menu-item[href]');
    
    navItems.forEach(function(item) {
      const href = item.getAttribute('href');
      // Remove leading slash for comparison
      const itemPath = href.replace(/^\//, '');
      const currentPathClean = currentPath.replace(/^\//, '');
      
      if (currentPathClean === itemPath || currentPathClean.endsWith('/' + itemPath)) {
        item.classList.add('active');
      }
    });
  }
  
  // Load navigation when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNavigation);
  } else {
    loadNavigation();
  }
})();

