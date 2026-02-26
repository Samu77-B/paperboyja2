# Navigation & Cart Fix Instructions

## Problem
The shopping cart is not displaying and the navigation needs to work across all pages.

## Solution

### Step 1: Fix the Cart Display on Index.html

The cart CSS has been updated in `css/modern-nav.css` to force the cart to display. **Refresh your browser and hard reload** (Ctrl+Shift+R or Cmd+Shift+R) to clear cache.

If the cart still doesn't show, add this to the `<head>` section of index.html after the modern-nav.css link:

```html
<style>
  /* Force cart to display */
  .ec-cart-widget {
    display: block !important;
    visibility: visible !important;
    min-height: 30px;
  }
</style>
```

### Step 2: Make Navigation Work Across All Pages

Since your website uses `.html` files, you have two options:

#### Option A: Convert to PHP (Recommended - works on server)

1. **Rename your HTML files to PHP:**
   - `index.html` → `index.php`
   - `contact.html` → `contact.php`
   - etc.

2. **Add this at the very top of each PHP file** (before `<!DOCTYPE html>`):
   ```php
   <?php
   // Set the root path based on current directory depth
   $current_dir = dirname($_SERVER['PHP_SELF']);
   $depth = substr_count($current_dir, '/') - 1;
   $root_path = str_repeat('../', max(0, $depth));
   ?>
   ```

3. **Replace the entire navigation HTML** (from `<!-- Modern Navigation Bar -->` to `</header>`) with:
   ```php
   <?php include($root_path . 'includes/nav.php'); ?>
   ```

4. **Add Ecwid scripts right after** (if not already there):
   ```html
   <script data-cfasync="false" type="text/javascript" src="https://app.ecwid.com/script.js?64309912&data_platform=code&data_date=2021-08-11" charset="utf-8"></script>
   <script>Ecwid.init();</script>
   ```

5. **Update .htaccess** to handle .html URLs redirecting to .php:
   ```apache
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME}.php -f
   RewriteRule ^(.*)\.html$ $1.php [L]
   ```

#### Option B: Copy/Paste Navigation (Works without server)

If you can't use PHP or want to keep .html files:

1. Copy the entire navigation section from `index.html` (lines 384-615)
2. Paste it into each HTML file where you want the navigation
3. Update the links based on folder depth:
   - **Root pages** (index.html, contact.html): Keep links as-is
   - **Subdirectory pages** (business-products/*.html): Add `../` before each link
   - Example: `href="index.html"` becomes `href="../index.html"`

### Step 3: Verify Cart Works

After implementing the navigation:

1. Clear browser cache (Ctrl+Shift+Delete)
2. Reload the page
3. The cart icon should appear in the top right
4. It may take 2-3 seconds to load after page loads

### Troubleshooting

**Cart still not showing?**

Check browser console (F12) for errors. Common issues:

1. **Ecwid script blocked**: Make sure `https://app.ecwid.com/script.js` is loading
2. **Ecwid.init() not called**: Ensure the Ecwid script is running AFTER the navigation HTML
3. **CSS conflict**: Add `!important` to cart display rules (see Step 1)

**Links broken on some pages?**

- Check that `../` is added correctly based on folder depth
- Root level: no `../`
- One level deep: `../`
- Two levels deep: `../../`

### Test Checklist

- [ ] Navigation appears on page
- [ ] Shopping cart icon visible in top right
- [ ] Cart shows item count when products added
- [ ] Services mega menu opens smoothly
- [ ] All links work from current page
- [ ] Search icon opens search overlay
- [ ] Mobile menu works on small screens

### Files Modified

1. `css/modern-nav.css` - Added cart display rules
2. `includes/nav.php` - Created PHP include file
3. `index.html` - Has working navigation (for reference)

### Need Help?

If converting to PHP, test on ONE page first (like index.html → index.php) before converting all pages.

