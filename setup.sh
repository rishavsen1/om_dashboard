#!/bin/bash

echo "🚀 Setting up Redeployable Value Dashboard..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 To start the application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the app: python app.py"
echo "   3. Open browser to: http://localhost:5000"
echo ""
echo "💡 To deactivate virtual environment later, just run: deactivate"
