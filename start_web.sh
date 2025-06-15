#!/bin/bash
# Startup script for trend_spotter web interface

echo "Starting trend_spotter web interface..."
echo "======================================"

# Add Google Cloud SDK to PATH
export PATH="$HOME/google-cloud-sdk/bin:$PATH"

# Navigate to project directory
cd "$HOME/trend_spotter"

# Activate virtual environment
source myenv/bin/activate

# Check if all dependencies are working
echo "✅ Checking Vertex AI configuration..."
python test_vertex_ai.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Starting web interface on http://localhost:8080"
    echo "Press Ctrl+C to stop"
    echo ""
    
    # Start the web interface
    python -m google.adk.cli web . --port 8080
else
    echo "❌ Vertex AI configuration failed. Please check your setup."
    exit 1
fi

