#!/bin/bash

# 🚀 CONVERGENCE SETUP SCRIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Icons
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="💡"
LOCK="🔐"

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ▄████▄   ▒█████   ███▄    █ ██▒   █▓▓█████  ██▀███    ▄████ ║"
echo "║ ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █▓██░   █▒▓█   ▀ ▓██ ▒ ██▒ ██▒ ▀█▒║"
echo "║ ▒▓█    ▄ ▒██░  ██▒▓██  ▀█ ██▒▓██  █▒░▒███   ▓██ ░▄█ ▒▒██░▄▄▄░║"
echo "║ ▒▓▓▄ ▄██▒▒██   ██░▓██▒  ▐▌██▒ ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ░▓█  ██▓║"
echo "║ ▒ ▓███▀ ░░ ████▓▒░▒██░   ▓██░  ▒▀█░  ░▒████▒░██▓ ▒██▒░▒▓███▀▒║"
echo "║ ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒   ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░ ░▒   ▒ ║"
echo "║   ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒░  ░ ░░   ░ ░  ░  ░▒ ░ ▒░  ░   ░ ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${BLUE}${ROCKET} Initializing Convergence Setup...${NC}\n"

# Function to print status
print_status() {
    echo -e "${BLUE}${INFO} $1${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING} $1${NC}"
}

# Check Python version
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
print_status "Installing dependencies..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    print_success "Development dependencies installed"
else
    pip install -r requirements.txt
    print_success "Dependencies installed"
fi

# Create output directory
print_status "Creating output directory..."
mkdir -p output
print_success "Output directory ready"

# Check for .env file
print_status "Checking environment configuration..."
if [ -f ".env" ]; then
    print_success "Environment file found"
else
    print_warning "No .env file found"
    echo -e "${YELLOW}   Creating .env.example file...${NC}"
    
    cat > .env.example << EOF
# ${LOCK} CONVERGENCE ENVIRONMENT CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# OpenAI API Key (required)
OPENAI_API_KEY=your-openai-api-key-here

# Environment name (optional)
ENVIRONMENT=development
EOF
    
    print_success ".env.example created"
    print_warning "Please copy .env.example to .env and add your OPENAI_API_KEY"
fi

# Self-healing check
print_status "Running self-healing checks..."

# Check if OpenAI key is set
if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY=your-openai-api-key-here" .env || ! grep -q "OPENAI_API_KEY=" .env; then
        print_warning "OPENAI_API_KEY not configured in .env file"
    else
        print_success "OPENAI_API_KEY configured"
    fi
fi

# Make scripts executable
if [ -d "scripts" ]; then
    print_status "Making scripts executable..."
    chmod +x scripts/*.sh 2>/dev/null || true
    print_success "Scripts are executable"
fi

echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           ${CHECK} SETUP COMPLETED SUCCESSFULLY! ${CHECK}              ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${CYAN}Next steps:${NC}"
echo -e "  1. ${YELLOW}Configure your OPENAI_API_KEY in .env file${NC}"
echo -e "  2. ${BLUE}Run tests: ${NC}./scripts/test.sh"
echo -e "  3. ${BLUE}Start CLI: ${NC}python -m convergence --help"
echo -e "  4. ${BLUE}Start API: ${NC}uvicorn convergence.api.app:app --reload"

echo -e "\n${CYAN}${ROCKET} Ready to converge! ${NC}\n"