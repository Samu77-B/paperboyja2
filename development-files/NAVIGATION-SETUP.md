# Modern Navigation Component - Setup Guide

## Overview
The navigation is now a reusable component that can be easily added to any page on your website.

## Files Created
1. **nav-component.html** - The HTML structure of the navigation
2. **css/modern-nav.css** - All navigation styles
3. **js/nav-loader.js** - JavaScript to load and initialize the navigation

## How to Add Navigation to Any Page

### Step 1: Add CSS Link
In the `<head>` section, add the modern navigation CSS:

```html
<link href="/css/modern-nav.css" rel="stylesheet" type="text/css">
```

**Important:** Use `/css/modern-nav.css` (with leading slash) so it works from any directory.

### Step 2: Add Placeholder & Loader Script
At the beginning of the `<body>` tag (where you want the nav to appear):

```html
<!-- Navigation Component Placeholder -->
<div id="nav-placeholder"></div>

<!-- Load Navigation Component -->
<script src="/js/nav-loader.js"></script>
```

### Step 3: Ecwid Scripts (if using cart/search)
After the nav loader, add Ecwid scripts:

```html
<!-- Ecwid Scripts -->
<script data-cfasync="false" type="text/javascript" src="https://app.ecwid.com/script.js?64309912&data_platform=code&data_date=2021-08-11" charset="utf-8"></script>
<script type="text/javascript">
  Ecwid.init();
</script>
```

## Complete Example

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Your Page Title</title>
  
  <!-- Your existing CSS -->
  <link href="/css/normalize.css" rel="stylesheet" type="text/css">
  <link href="/css/webflow.css" rel="stylesheet" type="text/css">
  <link href="/css/pbja.webflow.css" rel="stylesheet" type="text/css">
  
  <!-- Modern Navigation CSS -->
  <link href="/css/modern-nav.css" rel="stylesheet" type="text/css">
</head>
<body>
  <!-- Navigation Component -->
  <div id="nav-placeholder"></div>
  <script src="/js/nav-loader.js"></script>
  
  <!-- Ecwid Scripts -->
  <script data-cfasync="false" type="text/javascript" src="https://app.ecwid.com/script.js?64309912&data_platform=code&data_date=2021-08-11" charset="utf-8"></script>
  <script type="text/javascript">
    Ecwid.init();
  </script>
  
  <!-- Your page content here -->
  
</body>
</html>
```

## Features

### Automatic Active State
The navigation automatically highlights the current page based on the URL.

### Cart Styling Protection
The cart widget styling is isolated to prevent conflicts with Ecwid product pages.

### All Links Use Absolute Paths
All navigation links start with `/` so they work correctly from any page depth:
- Root page: `/index.html`
- Subdirectory: `/business-products/business-cards.html`

### Responsive Design
- Desktop: Full mega menu with all categories
- Mobile: Hamburger menu with collapsible services

## Customization

### To Update Navigation
Edit **nav-component.html** - changes will automatically appear on all pages.

### To Update Styles
Edit **css/modern-nav.css** - styles will update across all pages.

### To Update Functionality
Edit **js/nav-loader.js** - behavior changes will apply everywhere.

## Troubleshooting

### Navigation Not Appearing
1. Check that `/nav-component.html` exists in the root directory
2. Verify the path to `/js/nav-loader.js` is correct
3. Check browser console for errors

### Links Not Working
- All links in nav-component.html use absolute paths starting with `/`
- This ensures they work from any page location

### Cart Styling Issues
The cart widget has CSS isolation rules in `modern-nav.css`:
```css
.nav-cart-wrapper .ec-cart-widget {
  all: initial;
  display: block;
}
```

If you still see styling conflicts on product pages, these rules can be adjusted.

## Testing Checklist
- [ ] Navigation appears on page
- [ ] All links work correctly
- [ ] Services mega menu opens and closes smoothly
- [ ] Cart widget displays correctly
- [ ] Search overlay opens when clicking search icon
- [ ] Mobile menu works on smaller screens
- [ ] Current page is highlighted in navigation

