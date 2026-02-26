// Auto-update Copyright Year
// This script automatically updates the copyright year in all footer elements
(function() {
  'use strict';
  
  // Get current year
  const currentYear = new Date().getFullYear();
  
  // Function to update copyright year
  function updateCopyrightYear() {
    // Find all copyright elements (elements with class "text-block-27" that contain "Copyright")
    const copyrightElements = document.querySelectorAll('.text-block-27');
    
    copyrightElements.forEach(function(element) {
      const text = element.textContent || element.innerText;
      
      // Check if this element contains "Copyright"
      if (text.includes('Copyright')) {
        // Replace any 4-digit year (1900-2099) with current year
        const updatedText = text.replace(/\b(19|20)\d{2}\b/g, currentYear);
        element.textContent = updatedText;
      }
    });
  }
  
  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateCopyrightYear);
  } else {
    updateCopyrightYear();
  }
})();
