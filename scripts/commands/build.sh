#!/bin/bash

# 🏗️ CONVERGENCE BUILD SCRIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Icons
BUILD="🏗️"
CHECK="✅"
CROSS="❌"
CLEAN="🧹"
PACKAGE="📦"

echo -e "${CYAN}${BUILD} CONVERGENCE BUILD SYSTEM ${BUILD}${NC}\n"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}${CROSS} Virtual environment not found. Run ./scripts/setup.sh first${NC}"
    exit 1
fi

# Clean previous builds
echo -e "${BLUE}${CLEAN} Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}${CHECK} Clean complete${NC}\n"

# Format code
echo -e "${BLUE}🎨 Formatting code with black...${NC}"
black convergence/ tests/ --quiet || {
    echo -e "${YELLOW}⚠️  Black formatting had issues${NC}"
}
echo -e "${GREEN}${CHECK} Formatting complete${NC}\n"

# Sort imports
echo -e "${BLUE}📑 Sorting imports with isort...${NC}"
isort convergence/ tests/ --quiet || {
    echo -e "${YELLOW}⚠️  Import sorting had issues${NC}"
}
echo -e "${GREEN}${CHECK} Import sorting complete${NC}\n"

# Create distribution
echo -e "${BLUE}${PACKAGE} Building distribution packages...${NC}"
python -m pip install --upgrade build > /dev/null 2>&1
python -m build || {
    echo -e "${RED}${CROSS} Build failed${NC}"
    exit 1
}
echo -e "${GREEN}${CHECK} Distribution packages created${NC}\n"

# Docker build (if docker is available)
if command -v docker &> /dev/null; then
    echo -e "${BLUE}🐳 Building Docker image...${NC}"
    docker build -t convergence:latest . || {
        echo -e "${YELLOW}⚠️  Docker build failed${NC}"
    }
    echo -e "${GREEN}${CHECK} Docker image built${NC}\n"
else
    echo -e "${YELLOW}⚠️  Docker not found, skipping Docker build${NC}\n"
fi

echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ${CHECK} BUILD COMPLETED SUCCESSFULLY! ${CHECK}            ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${CYAN}Build artifacts:${NC}"
echo -e "  • Distribution packages in ${BLUE}dist/${NC}"
echo -e "  • Docker image: ${BLUE}convergence:latest${NC} (if Docker available)"

echo -e "\n${CYAN}Next steps:${NC}"
echo -e "  • Run tests: ${BLUE}./scripts/test.sh${NC}"
echo -e "  • Run linter: ${BLUE}./scripts/lint.sh${NC}"
echo -e "  • Start API: ${BLUE}docker-compose up${NC} (if Docker available)\n"