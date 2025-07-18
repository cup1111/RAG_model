#!/bin/bash

# AI Code Assistant - Frontend Startup Script
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

# Check Node.js version
check_node_version() {
    print_info "Checking Node.js version..."
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 16.0.0 or higher first."
        print_info "Download URL: https://nodejs.org/"
        exit 1
    fi
    
    node_version=$(node -v | sed 's/v//')
    required_version="16.0.0"
    
    if [ "$(printf '%s\n' "$required_version" "$node_version" | sort -V | head -n1)" = "$required_version" ]; then
        print_success "Node.js version check passed: $node_version"
    else
        print_error "Node.js version too low: $node_version, requires 16.0.0 or higher"
        exit 1
    fi
}

# Check npm
check_npm() {
    print_info "Checking npm..."
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    npm_version=$(npm -v)
    print_success "npm version: $npm_version"
}

# Check frontend directory
check_frontend_dir() {
    print_info "Checking frontend project directory..."
    
    if [ ! -d "frontend" ]; then
        print_error "frontend directory does not exist. Please ensure you're running this script from the project root directory"
        exit 1
    fi
    
    if [ ! -f "frontend/package.json" ]; then
        print_error "package.json file does not exist. Frontend project may be incomplete"
        exit 1
    fi
    
    print_success "Frontend project directory check passed"
}

# Install dependencies
install_dependencies() {
    print_info "Checking and installing frontend dependencies..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_warning "node_modules does not exist, installing dependencies..."
        npm install
        print_success "Dependencies installed successfully"
    else
        print_info "Checking if dependencies need updating..."
        npm install
        print_success "Dependency check completed"
    fi
    
    cd ..
}

# Check port availability
check_port() {
    local port=5173
    print_info "Checking if port $port is available..."
    
    if command -v lsof &> /dev/null; then
        # macOS/Linux
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            print_warning "Port $port is already in use. Please close the program using this port"
            print_info "You can use the following command to see which process is using the port:"
            print_info "lsof -i :$port"
            exit 1
        fi
    elif command -v netstat &> /dev/null; then
        # Windows
        if netstat -an | grep ":$port " | grep LISTEN >/dev/null 2>&1; then
            print_warning "Port $port is already in use. Please close the program using this port"
            exit 1
        fi
    else
        print_warning "Unable to check port availability. Please manually confirm if port $port is available"
    fi
    
    print_success "Port $port is available"
}

# Start frontend service
start_frontend() {
    print_info "Starting frontend service..."
    
    cd frontend
    
    print_success "Frontend service starting..."
    print_info "Service URL: http://localhost:5173"
    print_info "Press Ctrl+C to stop the service"
    print_info ""
    print_info "Tip: Make sure the backend service is also running (http://localhost:3000)"
    
    # Start development server
    npm run dev
}

# Show help information
show_help() {
    echo "=========================================="
    echo "    AI Code Assistant - Frontend Startup"
    echo "=========================================="
    echo ""
    echo "Usage: ./start-frontend.sh [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help      Show this help information"
    echo "  --check-only    Check environment only, do not start service"
    echo ""
    echo "Examples:"
    echo "  ./start-frontend.sh          # Start frontend service"
    echo "  ./start-frontend.sh --help   # Show help"
    echo "  ./start-frontend.sh --check-only  # Check environment only"
    echo ""
}

# Check environment only
check_environment_only() {
    echo "=========================================="
    echo "    AI Code Assistant - Environment Check"
    echo "=========================================="
    echo ""
    
    check_node_version
    check_npm
    check_frontend_dir
    install_dependencies
    check_port
    
    print_success "Environment check completed. All dependencies are ready!"
    print_info "You can now run ./start-frontend.sh to start the frontend service"
}

# Main function
main() {
    # Parse command line arguments
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        --check-only)
            check_environment_only
            exit 0
            ;;
        "")
            # No arguments, normal startup
            ;;
        *)
            print_error "Unknown argument: $1"
            show_help
            exit 1
            ;;
    esac
    
    echo "=========================================="
    echo "    AI Code Assistant - Frontend Startup"
    echo "=========================================="
    echo ""
    
    # Check if in correct directory
    if [ ! -d "frontend" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Execute check steps
    check_node_version
    check_npm
    check_frontend_dir
    install_dependencies
    check_port
    
    # Start the service
    start_frontend
}

# Handle Ctrl+C signal
trap 'echo ""; print_warning "Stopping frontend service..."; exit 0' INT

# Run main function
main "$@" 