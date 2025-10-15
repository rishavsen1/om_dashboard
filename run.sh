#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if venv activation worked
if [ $? -ne 0 ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

echo "🚀 Starting Redeployable Value Dashboard..."
echo "📍 Server will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Run the Flask application
python app.py
