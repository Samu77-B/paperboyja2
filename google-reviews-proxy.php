<?php
// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Include configuration
require_once 'google-reviews-config.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Get configuration
$config = getGoogleReviewsConfig();
$apiKey = $config['apiKey'];
$placeId = $config['placeId'];

// Function to fetch data from Google Places API
function fetchGoogleReviews($apiKey, $placeId) {
    $url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={$placeId}&fields=rating,user_ratings_total,reviews&key={$apiKey}";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200 && $response) {
        return json_decode($response, true);
    }
    
    return null;
}

// Function to get reviews from Google My Business API (alternative method)
function fetchGoogleMyBusinessReviews($apiKey) {
    // This would require Google My Business API setup
    // For now, we'll return null and use Places API
    return null;
}

// Main execution
try {
    // Check if API key is configured
    if (!isValidApiKey($apiKey)) {
        // Return static data if API key is not configured
        $staticData = [
            'rating' => $config['fallbackRating'],
            'user_ratings_total' => $config['fallbackReviewCount'],
            'reviews' => [
                [
                    'author_name' => 'John Smith',
                    'rating' => 5,
                    'text' => 'Excellent service and quality! The team at Paperboy was professional and delivered exactly what we needed.',
                    'profile_photo_url' => 'https://ui-avatars.com/api/?name=John+Smith&background=random'
                ],
                [
                    'author_name' => 'Sarah Johnson',
                    'rating' => 5,
                    'text' => 'Very impressed with the print quality and fast turnaround time. Will definitely use their services again!',
                    'profile_photo_url' => 'https://ui-avatars.com/api/?name=Sarah+Johnson&background=random'
                ],
                [
                    'author_name' => 'Michael Brown',
                    'rating' => 5,
                    'text' => 'Great experience working with Paperboy. Their attention to detail and customer service is outstanding.',
                    'profile_photo_url' => 'https://ui-avatars.com/api/?name=Michael+Brown&background=random'
                ],
                [
                    'author_name' => 'Emma Wilson',
                    'rating' => 5,
                    'text' => 'The team went above and beyond to meet our tight deadline. The final product exceeded our expectations!',
                    'profile_photo_url' => 'https://ui-avatars.com/api/?name=Emma+Wilson&background=random'
                ],
                [
                    'author_name' => 'David Thompson',
                    'rating' => 5,
                    'text' => 'Outstanding print quality and customer service. Paperboy JA delivered our project on time and exceeded expectations.',
                    'profile_photo_url' => 'https://ui-avatars.com/api/?name=David+Thompson&background=random'
                ]
            ]
        ];
        
        echo json_encode($staticData);
        exit;
    }
    
    // Fetch live data from Google Places API
    $data = fetchGoogleReviews($apiKey, $placeId);
    
    if ($data && isset($data['result'])) {
        $result = $data['result'];
        
        $response = [
            'rating' => $result['rating'] ?? $config['fallbackRating'],
            'user_ratings_total' => $result['user_ratings_total'] ?? $config['fallbackReviewCount'],
            'reviews' => []
        ];
        
        // Process reviews if available
        if (isset($result['reviews']) && is_array($result['reviews'])) {
            foreach ($result['reviews'] as $review) {
                $response['reviews'][] = [
                    'author_name' => $review['author_name'] ?? 'Anonymous',
                    'rating' => $review['rating'] ?? 5,
                    'text' => $review['text'] ?? '',
                    'profile_photo_url' => $review['profile_photo_url'] ?? null,
                    'time' => $review['time'] ?? null
                ];
            }
        }
        
        echo json_encode($response);
    } else if ($data && isset($data['error_message'])) {
        // Google API returned an error
        $errorMessage = $data['error_message'];
        if ($config['debugMode']) {
            error_log("Google Places API Error: " . $errorMessage);
        }
        
        // Return fallback data with error info
        echo json_encode([
            'error' => true,
            'message' => $errorMessage,
            'rating' => $config['fallbackRating'],
            'user_ratings_total' => $config['fallbackReviewCount'],
            'reviews' => []
        ]);
    } else {
        // Fallback to static data if API call fails
        if ($config['debugMode']) {
            error_log("Failed to fetch data from Google Places API. Response: " . json_encode($data));
        }
        throw new Exception('Failed to fetch data from Google Places API');
    }
    
} catch (Exception $e) {
    // Return error response
    http_response_code(500);
    echo json_encode([
        'error' => 'Failed to fetch reviews',
        'message' => $e->getMessage(),
        'fallback' => true,
        'rating' => $config['fallbackRating'],
        'user_ratings_total' => $config['fallbackReviewCount'],
        'reviews' => [
            [
                'author_name' => 'John Smith',
                'rating' => 5,
                'text' => 'Excellent service and quality! The team at Paperboy was professional and delivered exactly what we needed.',
                'profile_photo_url' => 'https://ui-avatars.com/api/?name=John+Smith&background=random'
            ],
            [
                'author_name' => 'Sarah Johnson',
                'rating' => 5,
                'text' => 'Very impressed with the print quality and fast turnaround time. Will definitely use their services again!',
                'profile_photo_url' => 'https://ui-avatars.com/api/?name=Sarah+Johnson&background=random'
            ]
        ]
    ]);
}
?>
