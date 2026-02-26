# Navigation Menu Deployment Script

## Purpose
This Python script (`deploy_menu.py`) automatically deploys the navigation menu from `index.html` to all other HTML pages in the website, ensuring consistency across the entire site.

## Usage

### Basic Usage
```bash
python deploy_menu.py
```

### What It Does
1. Extracts the navigation menu structure from `index.html`
2. Finds all HTML files in the website (excluding backup directories)
3. Removes old navigation elements from each file
4. Inserts the new navigation menu with properly adjusted paths
5. Provides a detailed summary of the operation

## Features

### Automatic Path Adjustment
The script intelligently adjusts relative paths based on each file's location:
- Root level files: `images/`, `css/`, `index.html`
- Subdirectory files: `../images/`, `../css/`, `../index.html`
- Nested subdirectories: `../../images/`, etc.

### Components Deployed
- **Desktop Navigation:** Full horizontal menu with mega dropdown
- **Mobile Navigation:** Hamburger menu with mobile-optimized layout
- **Styles:** CSS links and inline styles for proper display
- **Scripts:** JavaScript for interactivity (search, mobile menu, mega menu)
- **E-commerce:** Ecwid cart widget integration

### Safety Features
- Excludes backup and hidden directories
- Only modifies HTML files (skips other file types)
- Provides detailed logging of all operations
- Can be run multiple times safely (idempotent)

## Requirements
- Python 3.x (no additional packages required)
- Must be run from the website root directory

## Output
The script provides:
- Progress indicator for each file
- Summary statistics (updated, skipped, errors)
- Clear success/failure messages

## Example Output
```
======================================================================
Navigation Menu Deployment Script
======================================================================

Root directory: C:\Websites\Paperboy\Website 25\Working Site
Extracting menu from: ...\index.html

✓ Successfully extracted menu structure

Finding HTML files...
✓ Found 105 HTML files to update

Updating files:
----------------------------------------------------------------------
✓ Updated: contact.html
✓ Updated: business-products/business-cards.html
...

======================================================================
Summary:
  Total files found: 105
  Successfully updated: 104
  Skipped (no changes): 1
  Errors: 0
======================================================================

✓ Menu deployment completed successfully!
```

## When to Use
Run this script whenever you:
- Update the navigation menu in `index.html`
- Add new menu items
- Change menu styling
- Modify menu JavaScript functionality
- Need to ensure all pages have consistent navigation

## Excluded Directories
The script automatically skips:
- `backup_html_files/`
- `build/`
- `hidden/`
- `node_modules/`
- `.git/`

## Troubleshooting

### Script Not Found
Make sure you're in the website root directory where `deploy_menu.py` is located.

### Permission Errors
Ensure you have write permissions for all HTML files in the directory.

### Path Issues
The script assumes standard directory structure. If you have custom paths, you may need to adjust the `adjust_paths_for_depth()` function.

## Technical Details

### Files Modified
The script modifies:
- Navigation HTML structure
- CSS links in `<head>`
- JavaScript at end of `<body>`
- Inline styles for cart widget and hamburger menu

### Files Preserved
The script does NOT modify:
- Page-specific content
- Other scripts and styles
- Meta tags
- Page structure outside navigation

## Maintenance
To update the script's behavior, edit `deploy_menu.py` and modify:
- `extract_menu_from_index()` - Changes what gets extracted
- `adjust_paths_for_depth()` - Changes path adjustment logic
- `find_html_files()` - Changes which files are processed

## Support
For issues or questions, refer to `MENU_DEPLOYMENT_SUMMARY.md` for detailed information about the deployment process.

