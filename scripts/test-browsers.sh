#!/bin/bash

# Browser Testing Script
# This script simulates different browsers making requests to the nginx server

SERVER_URL=${1:-"http://localhost:8080"}

echo "🧪 Starting browser simulation tests against: $SERVER_URL"
echo "=================================================="

# Function to make a request with specific user agent
make_request() {
    local user_agent="$1"
    local browser_name="$2"
    local url="$3"
    local method="${4:-GET}"
    local extra_headers="${5:-}"
    
    echo "Testing $browser_name..."
    
    if [ "$method" = "POST" ]; then
        curl -s -X POST \
             -H "User-Agent: $user_agent" \
             -H "Accept: application/json, text/html, */*" \
             -H "Accept-Language: en-US,en;q=0.9" \
             -H "Accept-Encoding: gzip, deflate" \
             -H "Connection: keep-alive" \
             -H "Content-Type: application/json" \
             $extra_headers \
             -d '{"test": "browser-simulation", "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}' \
             "$SERVER_URL$url" > /dev/null
    else
        curl -s -H "User-Agent: $user_agent" \
             -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
             -H "Accept-Language: en-US,en;q=0.5" \
             -H "Accept-Encoding: gzip, deflate" \
             -H "Connection: keep-alive" \
             -H "Upgrade-Insecure-Requests: 1" \
             $extra_headers \
             "$SERVER_URL$url" > /dev/null
    fi
    
    echo "  ✓ $browser_name request completed"
}

echo "1. Testing different browsers on main page..."

# Chrome
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" "Chrome" "/"

# Firefox
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0" "Firefox" "/"

# Safari
make_request "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" "Safari" "/"

# Edge
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59" "Edge" "/"

echo ""
echo "2. Testing API endpoints..."

# Test JSON endpoint with different browsers
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" "Chrome" "/test/json"
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0" "Firefox" "/test/json"

# Test XML endpoint
make_request "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15" "Safari" "/test/xml"

echo ""
echo "3. Testing browser info API with POST..."

# Test browser info endpoint with POST requests
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" "Chrome" "/api/browser-info" "POST" "-H 'X-Browser-Test: Chrome-Simulation'"

make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0" "Firefox" "/api/browser-info" "POST" "-H 'X-Browser-Test: Firefox-Simulation'"

echo ""
echo "4. Testing large file download..."

# Test large file with different browsers
make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" "Chrome" "/test/large"

echo ""
echo "5. Testing multiple concurrent requests..."

# Simulate multiple requests from the same browser
for i in {1..3}; do
    make_request "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" "Chrome-$i" "/api/browser-info" &
done

wait

echo ""
echo "🎉 Browser simulation tests completed!"
echo "Check the nginx logs for detailed request information:"
echo "  docker-compose logs nginx-browser-test"
echo "  or check ./logs/browser_access.log"