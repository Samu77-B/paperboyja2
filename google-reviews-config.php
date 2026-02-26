<?php
// Google Reviews Configuration
// Copy this file to google-reviews-config.php and update with your actual API key

// Google Places API Configuration
define('GOOGLE_PLACES_API_KEY', 'AIzaSyADxPOxTWTSLPM_6x_1x1diOJOHeDEBQWY'); // Replace with your actual API key
define('GOOGLE_PLACE_ID', 'ChIJSWP3onlA244RzZO0K3PslDk'); // Paperboy JA Place ID

// Cache settings (optional - for performance)
define('CACHE_ENABLED', true);
define('CACHE_DURATION', 3600); // Cache for 1 hour (3600 seconds)

// Fallback settings
define('FALLBACK_RATING', 4.8);
define('FALLBACK_REVIEW_COUNT', 187);

// API request settings
define('API_TIMEOUT', 10); // seconds
define('MAX_REVIEWS', 10); // Maximum number of reviews to fetch

// Error reporting
define('DEBUG_MODE', true); // Set to true for detailed error messages

// Security settings
define('ALLOWED_ORIGINS', ['*']); // CORS settings - restrict as needed for production

// Function to validate API key
function isValidApiKey($apiKey) {
    return $apiKey && $apiKey !== 'YOUR_GOOGLE_PLACES_API_KEY' && strlen($apiKey) > 10;
}

// Function to get configuration
function getGoogleReviewsConfig() {
    return [
        'apiKey' => GOOGLE_PLACES_API_KEY,
        'placeId' => GOOGLE_PLACE_ID,
        'cacheEnabled' => CACHE_ENABLED,
        'cacheDuration' => CACHE_DURATION,
        'fallbackRating' => FALLBACK_RATING,
        'fallbackReviewCount' => FALLBACK_REVIEW_COUNT,
        'apiTimeout' => API_TIMEOUT,
        'maxReviews' => MAX_REVIEWS,
        'debugMode' => DEBUG_MODE
    ];
}
?>
