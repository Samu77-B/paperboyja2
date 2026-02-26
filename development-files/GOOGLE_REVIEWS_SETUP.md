# Google Reviews Live Feed Setup Guide

This guide explains how to set up the Google Reviews live feed integration for Paperboy JA's website.

## Overview

The Google Reviews integration allows your website to display live, up-to-date Google Reviews data including:
- Current rating (e.g., 4.8 stars)
- Total number of reviews (e.g., 151 Google Reviews)
- Individual review content with author names and ratings
- Automatic fallback to static data if the API is unavailable

## Files Created

1. **`google-reviews-proxy.php`** - Main proxy file that fetches data from Google Places API
2. **`google-reviews-config.php`** - Configuration file for API settings
3. **`test-google-reviews.html`** - Test page to verify the integration works
4. **`GOOGLE_REVIEWS_SETUP.md`** - This setup guide

## Setup Instructions

### Step 1: Get a Google Places API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Places API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Places API"
   - Click on it and press "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

### Step 2: Configure the API Key

1. Open `google-reviews-config.php`
2. Replace `YOUR_GOOGLE_PLACES_API_KEY` with your actual API key:
   ```php
   define('GOOGLE_PLACES_API_KEY', 'AIzaSyYourActualApiKeyHere');
   ```

### Step 3: Verify Place ID

The Place ID for Paperboy JA is already configured as:
```
ChIJN1t_tDeuEmsRUsoyG83frY4
```

To verify this is correct:
1. Go to [Google's Place ID Finder](https://developers.google.com/maps/documentation/places/web-service/place-id)
2. Search for "Paperboy JA" and your location
3. Copy the Place ID and update it in `google-reviews-config.php` if different

### Step 4: Test the Integration

1. Upload all files to your web server
2. Visit `test-google-reviews.html` in your browser
3. Click "Test Live Data" to verify the API connection works
4. If successful, you should see live rating and review data

## How It Works

### Frontend (JavaScript)
The existing JavaScript in `index.html` already includes:
- Functions to update rating display
- Functions to create review cards
- Carousel functionality using Slick Carousel
- Automatic fallback to static data if API fails

### Backend (PHP)
The `google-reviews-proxy.php` file:
1. Receives requests from the frontend
2. Fetches data from Google Places API
3. Processes and formats the response
4. Returns JSON data to the frontend
5. Includes error handling and fallback data

### Configuration Options

In `google-reviews-config.php`, you can adjust:

```php
// Cache settings (for performance)
define('CACHE_ENABLED', true);
define('CACHE_DURATION', 3600); // 1 hour

// Fallback settings
define('FALLBACK_RATING', 4.8);
define('FALLBACK_REVIEW_COUNT', 151);

// API settings
define('API_TIMEOUT', 10); // seconds
define('MAX_REVIEWS', 10); // Maximum reviews to fetch
```

## Security Considerations

### API Key Security
- **Never expose your API key in client-side code**
- The proxy approach keeps the API key secure on the server
- Consider restricting the API key to your domain in Google Cloud Console

### Rate Limiting
- Google Places API has usage limits
- The current setup includes basic error handling
- Consider implementing caching for production use

### CORS Settings
- Current setup allows all origins (`*`)
- For production, restrict to your domain:
  ```php
  define('ALLOWED_ORIGINS', ['https://yourdomain.com']);
  ```

## Troubleshooting

### Common Issues

1. **"API key not valid" error**
   - Verify your API key is correct
   - Ensure Places API is enabled in Google Cloud Console
   - Check if billing is enabled (required for Places API)

2. **"Place not found" error**
   - Verify the Place ID is correct
   - Use Google's Place ID Finder to get the correct ID

3. **CORS errors**
   - Ensure your server supports PHP
   - Check that the proxy file is accessible

4. **No reviews showing**
   - The Places API may not return all reviews
   - Check if the business has public reviews
   - Verify the Place ID corresponds to the correct business

### Testing

Use the test page (`test-google-reviews.html`) to:
- Verify API connectivity
- Test fallback functionality
- Debug any issues

## Performance Optimization

### Caching
Enable caching in the configuration to reduce API calls:
```php
define('CACHE_ENABLED', true);
define('CACHE_DURATION', 3600); // 1 hour
```

### Rate Limiting
Monitor your API usage in Google Cloud Console to avoid hitting limits.

## Maintenance

### Regular Tasks
1. Monitor API usage in Google Cloud Console
2. Check for any changes in Google's API terms
3. Update the Place ID if the business location changes
4. Review and update fallback data periodically

### Updates
- Keep the API key secure
- Monitor Google's API documentation for changes
- Test the integration regularly

## Support

If you encounter issues:
1. Check the browser console for JavaScript errors
2. Verify the API key and Place ID
3. Test with the provided test page
4. Check Google Cloud Console for API usage and errors

## Cost Considerations

- Google Places API has usage-based pricing
- Basic usage is typically free for small to medium websites
- Monitor usage in Google Cloud Console
- Consider implementing caching to reduce API calls

---

**Note**: This integration provides a live connection to Google Reviews while maintaining security and performance. The fallback system ensures your website always displays review information, even if the API is temporarily unavailable.
