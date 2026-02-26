#!/usr/bin/env python3
"""
Deploy Modern Navigation to All HTML Pages
Automatically adds the new navigation bar to all HTML files in the website
"""

import os
import re
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).parent
BACKUP_DIR = ROOT_DIR / "backup_html_files"
INDEX_FILE = ROOT_DIR / "index.html"

# Navigation markers
NAV_START_MARKER = "<!-- Modern Navigation Bar -->"
NAV_END_MARKER = "</header>"
ECWID_SCRIPT_START = "<!-- Ecwid Scripts -->"
NAV_JS_END = "<!-- Initialize inline search after page loads -->"

def create_backup():
    """Create backup directory for HTML files"""
    BACKUP_DIR.mkdir(exist_ok=True)
    print(f"[OK] Backup directory created: {BACKUP_DIR}")

def extract_navigation_from_index():
    """Extract the complete navigation section from index.html"""
    print(f"\nReading navigation from {INDEX_FILE.name}...")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find navigation section
    nav_start = content.find(NAV_START_MARKER)
    if nav_start == -1:
        raise Exception("Could not find navigation start marker in index.html")
    
    # Find the end of the navigation JavaScript (after the header closes)
    nav_js_end_pos = content.find(NAV_JS_END, nav_start)
    if nav_js_end_pos == -1:
        raise Exception("Could not find navigation end marker in index.html")
    
    # Find the end of the inline search script (complete section)
    script_end = content.find("</script>", nav_js_end_pos)
    nav_end = script_end + len("</script>")
    
    navigation_html = content[nav_start:nav_end]
    
    print(f"[OK] Navigation extracted ({len(navigation_html)} characters)")
    return navigation_html

def adjust_paths_for_depth(html, depth):
    """Adjust all paths in the HTML based on directory depth"""
    if depth == 0:
        return html
    
    # Create the path prefix
    prefix = "../" * depth
    
    # Patterns to replace
    patterns = [
        # href attributes
        (r'href="(?!http|#|/|mailto:|tel:)([^"]+)"', f'href="{prefix}\\1"'),
        # src attributes
        (r'src="(?!http|/|data:)([^"]+)"', f'src="{prefix}\\1"'),
    ]
    
    result = html
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)
    
    return result

def find_old_navigation(content):
    """Find old navigation patterns in HTML"""
    old_patterns = [
        (r'<header[^>]*class="[^"]*sticky-nav[^"]*".*?</header>', 'sticky-nav header'),
        (r'<div[^>]*class="[^"]*navbar w-nav[^"]*".*?</div>\s*</header>', 'navbar w-nav'),
        (r'<!-- Modern Navigation Bar -->.*?</script>\s*(?=<div|<!-- )', 'Modern Navigation'),
    ]
    
    for pattern, name in old_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.start(), match.end(), name
    
    return None, None, None

def get_folder_depth(file_path):
    """Calculate folder depth relative to root"""
    relative_path = file_path.relative_to(ROOT_DIR)
    return len(relative_path.parents) - 1

def has_ecwid_product(content):
    """Check if the page has embedded Ecwid products"""
    return 'data-cfasync="false"' in content and 'ecwid.com' in content.lower()

def process_html_file(file_path, navigation_template):
    """Process a single HTML file and add/update navigation"""
    print(f"\nProcessing: {file_path.relative_to(ROOT_DIR)}")
    
    # Skip index.html as it's our source
    if file_path.name == "index.html" and file_path.parent == ROOT_DIR:
        print("   [SKIP] Skipping source file (index.html)")
        return False
    
    # Create backup
    backup_path = BACKUP_DIR / file_path.relative_to(ROOT_DIR)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Backup original
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    # Calculate depth and adjust paths
    depth = get_folder_depth(file_path)
    print(f"   Folder depth: {depth}")
    
    adjusted_nav = adjust_paths_for_depth(navigation_template, depth)
    
    # Check for old navigation
    old_start, old_end, old_type = find_old_navigation(original_content)
    
    if old_start is not None:
        print(f"   [OK] Found old navigation ({old_type})")
        # Replace old navigation
        new_content = (
            original_content[:old_start] +
            adjusted_nav +
            original_content[old_end:]
        )
    else:
        # No old navigation found - insert after <body> tag
        print("   [INFO] No old navigation found, inserting new one")
        body_match = re.search(r'<body[^>]*>', original_content)
        if body_match:
            insert_pos = body_match.end()
            new_content = (
                original_content[:insert_pos] +
                "\n  " + adjusted_nav + "\n" +
                original_content[insert_pos:]
            )
        else:
            print("   [ERROR] Could not find <body> tag!")
            return False
    
    # Ensure CSS link is present
    if 'modern-nav.css' not in new_content:
        print("   [ADD] Adding modern-nav.css link")
        css_path = f"{'../' * depth}css/modern-nav.css"
        
        # Find </head> and insert before it
        head_end = new_content.find('</head>')
        if head_end != -1:
            css_link = f'  <link href="{css_path}" rel="stylesheet" type="text/css">\n  '
            new_content = new_content[:head_end] + css_link + new_content[head_end:]
    
    # Ensure cart display fix is present
    if '.ec-cart-widget' not in new_content or 'Force Cart Widget' not in new_content:
        print("   [ADD] Adding cart display fix")
        cart_css = f"""
  <!-- Force Cart Widget to Display -->
  <style>
    .ec-cart-widget {{
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      min-height: 30px !important;
    }}
    .ec-cart-widget * {{
      visibility: visible !important;
    }}
  </style>
  """
        head_end = new_content.find('</head>')
        if head_end != -1:
            new_content = new_content[:head_end] + cart_css + new_content[head_end:]
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   [OK] Updated successfully")
    return True

def find_all_html_files():
    """Find all HTML files in the website"""
    html_files = []
    exclude_dirs = {'backup_html_files', 'node_modules', '.git', 'build', 'hidden'}
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    
    return sorted(html_files)

def main():
    """Main execution function"""
    print("=" * 70)
    print("DEPLOYING MODERN NAVIGATION TO ALL HTML PAGES")
    print("=" * 70)
    
    try:
        # Step 1: Create backup
        create_backup()
        
        # Step 2: Extract navigation from index.html
        navigation_template = extract_navigation_from_index()
        
        # Step 3: Find all HTML files
        html_files = find_all_html_files()
        print(f"\nFound {len(html_files)} HTML files to process")
        
        # Step 4: Process each file
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for file_path in html_files:
            try:
                result = process_html_file(file_path, navigation_template)
                if result:
                    success_count += 1
                else:
                    skip_count += 1
            except Exception as e:
                print(f"   [ERROR]: {str(e)}")
                error_count += 1
        
        # Step 5: Summary
        print("\n" + "=" * 70)
        print("DEPLOYMENT SUMMARY")
        print("=" * 70)
        print(f"Successfully updated: {success_count} files")
        print(f"Skipped: {skip_count} files")
        print(f"Errors: {error_count} files")
        print(f"\nBackups saved to: {BACKUP_DIR}")
        print("\nDEPLOYMENT COMPLETE!")
        print("\nNext steps:")
        print("1. Test the navigation on index.html")
        print("2. Check a few other pages to verify links work")
        print("3. If everything looks good, you're done!")
        print("4. If you need to revert, restore files from backup_html_files/")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        print(f"Check that {INDEX_FILE} exists and has the navigation section")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

