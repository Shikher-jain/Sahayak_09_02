#!/bin/bash

# Sahayak Setup Script
# Complete setup for the AI Teaching Assistant

echo "============================================"
echo "🚀 Sahayak AI Teaching Assistant Setup"
echo "============================================"

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $(python --version)"

# Check if Cosdata is running
echo ""
echo "Checking Cosdata connection..."
if curl -s http://127.0.0.1:8443 > /dev/null 2>&1; then
    echo "✓ Cosdata is running"
else
    echo "⚠️  Cosdata is not running"
    echo ""
    echo "Please start Cosdata first:"
    echo "  start-cosdata"
    echo ""
    echo "Or use Docker:"
    echo "  docker run -d --name cosdata-server -p 8443:8443 -p 50051:50051 cosdataio/cosdata:latest"
    echo ""
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create data directory
mkdir -p data/pdf_storage
echo "✓ Created data directory"

echo ""
echo "============================================"
echo "✓ Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Cosdata (if not already running):"
echo "   start-cosdata"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   python -m uvicorn main:app --reload"
echo ""
echo "3. Start the frontend (in a new terminal):"
echo "   cd frontend"
echo "   streamlit run app.py"
echo ""
echo "4. Open http://localhost:8501 in your browser"
echo ""
