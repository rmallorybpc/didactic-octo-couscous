#!/bin/bash
# Setup script for Job Search AI Agent

set -e

echo "=========================================="
echo "Job Search AI Agent - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data
mkdir -p logs

# Copy environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - SLACK_BOT_TOKEN"
    echo "   - OPENAI_API_KEY (optional)"
    echo ""
else
    echo ""
    echo "✓ .env file already exists"
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x main.py demo.py setup.sh

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python3 demo.py (to test without API keys)"
echo "3. Run: python3 main.py --mode test (to test connections)"
echo "4. Run: python3 main.py --mode run-once (to run once)"
echo "5. Run: python3 main.py --mode schedule (to run daily)"
echo ""
