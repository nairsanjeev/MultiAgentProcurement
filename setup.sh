#!/bin/bash

# Setup Script for Procurement Agent System (Linux/Mac)
# This script helps automate the initial setup process

echo "========================================"
echo "Procurement Agent System - Setup Script"
echo "========================================"
echo ""

# Check Prerequisites
echo "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python not found. Please install Python 3.10 or higher."
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js found: $NODE_VERSION"
else
    echo "✗ Node.js not found. Please install Node.js 18 or higher."
    exit 1
fi

echo ""
echo "========================================"
echo "Setting up Backend..."
echo "========================================"

# Setup Backend
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies (with --pre flag)..."
pip install -r requirements.txt --pre

echo "Creating .env file from template..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file. Please edit it with your Azure credentials."
else
    echo "! .env file already exists. Skipping..."
fi

echo "✓ Backend setup complete!"
echo ""

# Setup Frontend
cd ../frontend

echo "========================================"
echo "Setting up Frontend..."
echo "========================================"

echo "Installing Node.js dependencies..."
npm install

echo "Creating .env.local file from template..."
if [ ! -f .env.local ]; then
    cp .env.local.example .env.local
    echo "✓ Created .env.local file."
else
    echo "! .env.local file already exists. Skipping..."
fi

echo "✓ Frontend setup complete!"
echo ""

# Return to root
cd ..

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Edit backend/.env with your Azure OpenAI credentials"
echo "2. Start the backend: cd backend && python main.py"
echo "3. In a new terminal, start the frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "For detailed instructions, see:"
echo "  - README.md for full documentation"
echo "  - QUICKSTART.md for quick start guide"
echo ""
echo "Happy coding! 🚀"
