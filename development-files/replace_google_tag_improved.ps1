$rootDir = "c:\Websites\Paperboy\Website 25\01\_public_html"
$htmlFiles = Get-ChildItem -Path $rootDir -Filter "*.html" -Recurse

$newGoogleTag = @"
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-947981377"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'AW-947981377');
  </script>
"@

$filesModified = 0
$tagsReplaced = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    $modified = $false
    
    # Replace Google Tag Manager in head section
    if ($content -match "<!-- Google Tag Manager -->") {
        $pattern = "(?s)<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->"
        $content = $content -replace $pattern, $newGoogleTag
        $tagsReplaced++
        $modified = $true
    }
    
    # Replace Google Analytics script blocks
    if ($content -match "googletagmanager.com/gtag/js\?id=G-") {
        $pattern = "(?s)<script async.*?googletagmanager.com/gtag/js\?id=G-.*?</script>\s*<script>\s*window\.dataLayer.*?gtag\('config', 'G-[^']*'\);\s*</script>"
        $content = $content -replace $pattern, $newGoogleTag
        $tagsReplaced++
        $modified = $true
    }
    
    # Replace Google Tag Manager noscript tags
    if ($content -match "Google Tag Manager \(noscript\)") {
        $pattern = "(?s)<!--\s*Google Tag Manager \(noscript\)\s*-->\s*<noscript>.*?</noscript>\s*<!--\s*End Google Tag Manager \(noscript\)\s*-->"
        $content = $content -replace $pattern, ""
        $tagsReplaced++
        $modified = $true
    }
    
    # Update any remaining gtag config calls
    if ($content -match "gtag\('config', 'G-[^']*'\)") {
        $pattern = "gtag\('config', 'G-[^']*'\)"
        $content = $content -replace $pattern, "gtag('config', 'AW-947981377')"
        $tagsReplaced++
        $modified = $true
    }
    
    # Save the file if changes were made
    if ($modified) {
        $filesModified++
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Updated: $($file.FullName)"
    }
}

Write-Host "Summary:"
Write-Host "Files modified: $filesModified"
Write-Host "Google tags replaced: $tagsReplaced"
