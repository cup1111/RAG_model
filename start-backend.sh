#!/bin/bash

# AI Code Assistant - Backend Startup Script
# Author: Zane Wang
# Email: 5finoilheater@gmail.com

set -e  # Exit on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
check_python_version() {
    print_info "Checking Python version..."
    
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed. Please install Python 3.8 or higher first."
        exit 1
    fi
    
    python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    required_version="3.8"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
        print_success "Python version check passed: $python_version"
    else
        print_error "Python version too low: $python_version, requires 3.8 or higher"
        exit 1
    fi
}

# Check virtual environment
check_venv() {
    print_info "Checking virtual environment..."
    
    if [ ! -d "python-backend/venv" ]; then
        print_warning "Virtual environment does not exist, creating..."
        cd python-backend
        python -m venv venv
        print_success "Virtual environment created successfully"
        cd ..
    else
        print_success "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source python-backend/venv/Scripts/activate
    else
        # macOS/Linux
        source python-backend/venv/bin/activate
    fi
    
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_info "Checking and installing Python dependencies..."
    
    cd python-backend
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt file does not exist"
        exit 1
    fi
    
    # Install dependencies
    pip install -r requirements.txt
    
    cd ..
    print_success "Dependencies installed successfully"
}

# Check environment variables
check_env() {
    print_info "Checking environment variable configuration..."
    
    if [ ! -f "python-backend/.env" ]; then
        print_warning ".env file does not exist, creating..."
        echo "OPENAI_API_KEY=your_openai_api_key_here" > python-backend/.env
        print_warning "Please edit python-backend/.env file to set your OpenAI API key"
        print_warning "Format: OPENAI_API_KEY=sk-your-actual-api-key"
    else
        print_success ".env file already exists"
    fi
}

# Start backend service
start_backend() {
    print_info "Starting backend service..."
    
    cd python-backend
    
    # Check if main.py exists
    if [ ! -f "main.py" ]; then
        print_error "main.py file does not exist"
        exit 1
    fi
    
    print_success "Backend service starting..."
    print_info "Service URL: http://localhost:3000"
    print_info "API Documentation: http://localhost:3000/docs"
    print_info "Press Ctrl+C to stop the service"
    
    # Start the service
    python main.py
}

# Main function
main() {
    echo "=========================================="
    echo "    AI Code Assistant - Backend Startup"
    echo "=========================================="
    echo ""
    
    # Check if in correct directory
    if [ ! -d "python-backend" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Execute check steps
    check_python_version
    check_venv
    activate_venv
    install_dependencies
    check_env
    
    # Start the service
    start_backend
}

# Handle Ctrl+C signal
trap 'echo ""; print_warning "Stopping backend service..."; exit 0' INT

# Run main function
main 