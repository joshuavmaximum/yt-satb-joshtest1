#!/bin/bash

echo "Setting up SATB Arranger Tool..."

# Check if Python 3.8+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "Error: Python 3.8 or higher is required (found $python_version)"
    exit 1
fi

# Update package manager
echo "Updating package manager..."
sudo apt-get update -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y ffmpeg

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download Spleeter models
echo "Pre-downloading Spleeter models..."
python3 -c "from spleeter.separator import Separator; Separator('spleeter:2stems')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the tool:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the web interface: streamlit run src/app.py"
echo "   OR"
echo "   Run the CLI: python src/main.py --youtube-url <URL>"
echo ""