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

$gtmPattern = '(?s)<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->'
$gaPattern = '(?s)<script async="" src="https://www.googletagmanager.com/gtag/js\?id=G-L53GKPJYJG"></script>.*?gtag\(''config'', ''G-L53GKPJYJG''\);</script>'

$filesModified = 0
$filesWithGTM = 0
$filesWithGA = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $originalContent = $content
    $modified = $false
    
    # Replace Google Tag Manager
    if ($content -match $gtmPattern) {
        $content = $content -replace $gtmPattern, $newGoogleTag
        $filesWithGTM++
        $modified = $true
    }
    
    # Replace Google Analytics
    if ($content -match $gaPattern) {
        $content = $content -replace $gaPattern, ""
        $filesWithGA++
        $modified = $true
    }
    
    # Update gtag config if it exists elsewhere in the file
    if ($content -match "gtag\('config', 'G-L53GKPJYJG'\);") {
        $content = $content -replace "gtag\('config', 'G-L53GKPJYJG'\);", "gtag('config', 'AW-947981377');"
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
Write-Host "Files with Google Tag Manager replaced: $filesWithGTM"
Write-Host "Files with Google Analytics replaced: $filesWithGA"
