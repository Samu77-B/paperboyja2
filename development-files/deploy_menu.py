#!/usr/bin/env python3
"""
Script to deploy the navigation menu from index.html to all other HTML pages.
This ensures consistent menu structure across the entire website.
"""

import os
import re
from pathlib import Path
from typing import Tuple, Optional

def extract_menu_from_index(index_path: str) -> Tuple[str, str, str]:
    """
    Extract the navigation menu, related styles, and scripts from index.html.
    
    Returns:
        Tuple of (menu_html, menu_styles, menu_scripts)
    """
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the modern navigation header
    menu_pattern = r'(<!-- Modern Navigation Bar -->.*?</header>)'
    menu_match = re.search(menu_pattern, content, re.DOTALL)
    menu_html = menu_match.group(1) if menu_match else None
    
    # Extract Ecwid scripts (including both the source script and initialization script)
    ecwid_pattern = r'(<!-- Ecwid Scripts -->.*?</script>\s*<script type="text/javascript">.*?</script>)'
    ecwid_match = re.search(ecwid_pattern, content, re.DOTALL)
    ecwid_scripts = ecwid_match.group(1) if ecwid_match else ""
    
    # Extract navigation JavaScript
    nav_js_pattern = r'(<!-- Navigation JavaScript -->.*?</script>)'
    nav_js_match = re.search(nav_js_pattern, content, re.DOTALL)
    nav_js = nav_js_match.group(1) if nav_js_match else ""
    
    # Extract inline search initialization script
    search_init_pattern = r'(<!-- Initialize inline search after page loads -->.*?</script>)'
    search_init_match = re.search(search_init_pattern, content, re.DOTALL)
    search_init = search_init_match.group(1) if search_init_match else ""
    
    menu_scripts = ecwid_scripts + "\n  \n  " + nav_js + "\n  \n  " + search_init
    
    # Extract menu-related styles from head
    # Looking for modern-nav.css link and Force Cart Widget styles
    modern_nav_css = '<link href="css/modern-nav.css" rel="stylesheet" type="text/css">'
    
    cart_widget_style = '''  <!-- Force Cart Widget to Display -->
  <style>
    .ec-cart-widget {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      min-height: 30px !important;
    }
    .ec-cart-widget * {
      visibility: visible !important;
    }
  </style>'''
    
    hamburger_style = '''  
  <!-- Hamburger Menu Styling -->
  <style>
    /* Override hamburger menu active state with brand blue */
    .w-nav-button.w--open {
      background-color: #00aeec !important;
      color: white !important;
      border-radius: 50px !important;
    }
    
    /* Make hamburger menu button smaller */
    .w-nav-button {
      padding: 13px !important;
      font-size: 20px !important;
    }
  </style>'''
    
    menu_styles = modern_nav_css + "\n  \n" + cart_widget_style + "\n" + hamburger_style
    
    return menu_html, menu_styles, menu_scripts


def adjust_paths_for_depth(html: str, depth: int) -> str:
    """
    Adjust relative paths in HTML based on directory depth.
    
    Args:
        html: HTML content with paths
        depth: Directory depth (0 for root, 1 for subdirectory, etc.)
    
    Returns:
        HTML with adjusted paths
    """
    if depth == 0:
        return html
    
    prefix = "../" * depth
    
    # Adjust image paths
    html = re.sub(r'src="images/', f'src="{prefix}images/', html)
    
    # Adjust href paths for internal links (but not external or anchor links)
    html = re.sub(r'href="(?!http|#|mailto|tel)([^"]*?\.html)"', f'href="{prefix}\\1"', html)
    
    # Adjust CSS paths
    html = re.sub(r'href="css/', f'href="{prefix}css/', html)
    
    # Adjust js paths
    html = re.sub(r'src="js/', f'src="{prefix}js/', html)
    
    return html


def get_directory_depth(file_path: str, root_dir: str) -> int:
    """
    Calculate the directory depth of a file relative to root.
    
    Args:
        file_path: Full path to the file
        root_dir: Root directory path
    
    Returns:
        Depth as integer (0 for root level)
    """
    rel_path = os.path.relpath(os.path.dirname(file_path), root_dir)
    if rel_path == '.':
        return 0
    return len(Path(rel_path).parts)


def update_html_file(file_path: str, menu_html: str, menu_styles: str, menu_scripts: str, root_dir: str) -> bool:
    """
    Update an HTML file with the new menu structure.
    
    Args:
        file_path: Path to the HTML file
        menu_html: Navigation menu HTML
        menu_styles: Menu-related styles
        menu_scripts: Menu-related scripts
        root_dir: Root directory of the website
    
    Returns:
        True if file was updated, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Calculate directory depth and adjust paths
        depth = get_directory_depth(file_path, root_dir)
        adjusted_menu_html = adjust_paths_for_depth(menu_html, depth)
        adjusted_menu_styles = adjust_paths_for_depth(menu_styles, depth)
        adjusted_menu_scripts = adjust_paths_for_depth(menu_scripts, depth)
        
        # Remove old navigation if it exists
        # Remove old modern navigation
        content = re.sub(
            r'<!-- Modern Navigation Bar -->.*?</header>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove old Ecwid scripts (including the comment and both script tags)
        content = re.sub(
            r'<!-- Ecwid Scripts -->.*?</script>\s*<script type="text/javascript">.*?</script>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Also remove any orphaned Ecwid.init() scripts that might be in the body
        content = re.sub(
            r'<script type="text/javascript">\s*Ecwid\.init\(\);\s*xSearch\("id=my-search-64309912"\);\s*</script>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove old Navigation JavaScript
        content = re.sub(
            r'<!-- Navigation JavaScript -->.*?</script>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove old inline search initialization
        content = re.sub(
            r'<!-- Initialize inline search after page loads -->.*?</script>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Ensure modern-nav.css is in head (remove all occurrences if they exist)
        content = re.sub(
            r'<link href="[^"]*?modern-nav\.css"[^>]*?>\s*',
            '',
            content
        )
        
        # Remove old cart widget styles if they exist (all occurrences)
        content = re.sub(
            r'<!-- Force Cart Widget to Display -->.*?</style>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove old hamburger menu styling if it exists (all occurrences)
        content = re.sub(
            r'<!-- Hamburger Menu Styling -->.*?</style>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Add menu styles to head (before </head>) - only replace first occurrence
        if '</head>' in content:
            content = content.replace('</head>', f'\n  {adjusted_menu_styles}\n  </head>', 1)
        
        # Add menu HTML after <body> tag
        body_pattern = r'(<body[^>]*>)'
        if re.search(body_pattern, content):
            content = re.sub(
                body_pattern,
                f'\\1\n  {adjusted_menu_html}\n',
                content,
                count=1
            )
        
        # Add menu scripts before closing body tag
        if '</body>' in content:
            # Find the position before </body>
            body_close_pos = content.rfind('</body>')
            content = content[:body_close_pos] + f'  {adjusted_menu_scripts}\n  ' + content[body_close_pos:]
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error updating {file_path}: {str(e)}")
        return False


def find_html_files(root_dir: str, exclude_dirs: list = None) -> list:
    """
    Find all HTML files in the directory tree.
    
    Args:
        root_dir: Root directory to search
        exclude_dirs: List of directory names to exclude
    
    Returns:
        List of HTML file paths
    """
    if exclude_dirs is None:
        exclude_dirs = ['backup_html_files', 'build', 'hidden', 'node_modules', '.git']
    
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from dirs list
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':  # Skip index.html itself
                html_files.append(os.path.join(root, file))
    
    return html_files


def main():
    """Main function to deploy menu to all pages."""
    # Get the script directory (should be the website root)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(root_dir, 'index.html')
    
    print("=" * 70)
    print("Navigation Menu Deployment Script")
    print("=" * 70)
    print()
    
    # Check if index.html exists
    if not os.path.exists(index_path):
        print(f"Error: index.html not found at {index_path}")
        return
    
    print(f"Root directory: {root_dir}")
    print(f"Extracting menu from: {index_path}")
    print()
    
    # Extract menu from index.html
    try:
        menu_html, menu_styles, menu_scripts = extract_menu_from_index(index_path)
        if not menu_html:
            print("Error: Could not extract menu from index.html")
            return
        print("✓ Successfully extracted menu structure")
        print()
    except Exception as e:
        print(f"Error extracting menu: {str(e)}")
        return
    
    # Find all HTML files
    print("Finding HTML files...")
    html_files = find_html_files(root_dir)
    print(f"✓ Found {len(html_files)} HTML files to update")
    print()
    
    # Update each file
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    print("Updating files:")
    print("-" * 70)
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        try:
            if update_html_file(file_path, menu_html, menu_styles, menu_scripts, root_dir):
                print(f"✓ Updated: {rel_path}")
                updated_count += 1
            else:
                print(f"○ Skipped (no changes): {rel_path}")
                skipped_count += 1
        except Exception as e:
            print(f"✗ Error: {rel_path} - {str(e)}")
            error_count += 1
    
    print()
    print("=" * 70)
    print("Summary:")
    print(f"  Total files found: {len(html_files)}")
    print(f"  Successfully updated: {updated_count}")
    print(f"  Skipped (no changes): {skipped_count}")
    print(f"  Errors: {error_count}")
    print("=" * 70)
    print()
    
    if error_count == 0:
        print("✓ Menu deployment completed successfully!")
    else:
        print("⚠ Menu deployment completed with some errors.")


if __name__ == "__main__":
    main()

