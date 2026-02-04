#!/bin/bash
# AI Native 研发平台 - Virtual Environment Setup Script for Linux/Mac

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Virtual environment setup complete!"
echo "========================================"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
