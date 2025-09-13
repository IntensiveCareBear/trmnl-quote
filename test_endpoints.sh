#!/bin/bash

echo "Testing TRMNL Quote Plugin Endpoints"
echo "===================================="

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s http://localhost:5000/health | python3 -m json.tool
echo ""

# Test quotes endpoint
echo "2. Testing quotes endpoint..."
curl -s http://localhost:5000/api/quotes | python3 -m json.tool
echo ""

# Test random quote endpoint
echo "3. Testing random quote endpoint..."
curl -s http://localhost:5000/api/quotes/random | python3 -m json.tool
echo ""

# Test TRMNL markup endpoint
echo "4. Testing TRMNL markup endpoint..."
curl -s http://localhost:5000/trmnl/markup | head -20
echo ""

# Test web interface
echo "5. Testing web interface..."
curl -s -I http://localhost:5000/ | head -5
echo ""

echo "All tests completed!"
