#!/bin/bash

# Quick Start Script for Nginx Browser Testing
# This script sets up and runs the complete testing environment

echo "🚀 Starting Nginx Browser Testing Environment"
echo "=============================================="

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose first."
    exit 1
fi

# Create logs directory
mkdir -p logs

echo "📦 Building and starting the nginx service..."
docker compose up -d

# Wait for service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 3

# Test if service is running
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ Service is running at http://localhost:8080"
    
    echo ""
    echo "🧪 Running browser simulation tests..."
    ./scripts/test-browsers.sh http://localhost:8080
    
    echo ""
    echo "📊 Analyzing generated logs..."
    python3 scripts/analyze-logs.py logs/browser_access.log --detailed
    
    echo ""
    echo "🎉 Setup complete! You can now:"
    echo "  - Visit http://localhost:8080 in different browsers"
    echo "  - Run './scripts/test-browsers.sh' for more tests"
    echo "  - Analyze logs with 'python3 scripts/analyze-logs.py logs/browser_access.log'"
    echo "  - Stop the service with 'docker compose down'"
    
else
    echo "❌ Service failed to start properly"
    echo "Check logs with: docker compose logs"
    exit 1
fi