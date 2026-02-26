$rootDir = "c:\Websites\Paperboy\Website 25\01\_public_html"
$htmlFiles = Get-ChildItem -Path $rootDir -Filter "*.html" -Recurse

$gtagEventCode = @"

  <!-- Google tag (gtag.js) event -->
  <script>
    gtag('event', 'newsletter_sign_up', {
      // <event_parameters>
    });
  </script>
"@

$filesModified = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Check if the file already has the newsletter_sign_up event code
    if ($content -match "gtag\('event', 'newsletter_sign_up'") {
        Write-Host "Skipping (already has newsletter_sign_up event code): $($file.FullName)"
        continue
    }
    
    # Find the end of the head section
    if ($content -match "</head>") {
        # Insert the gtag event code before the closing head tag
        $content = $content -replace "</head>", "$gtagEventCode</head>"
        
        # Save the file
        Set-Content -Path $file.FullName -Value $content
        $filesModified++
        Write-Host "Updated: $($file.FullName)"
    } else {
        Write-Host "Warning: No </head> tag found in $($file.FullName)"
    }
}

Write-Host "Summary:"
Write-Host "Files modified: $filesModified"
