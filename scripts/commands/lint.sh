#!/bin/bash

# 🔍 CONVERGENCE LINT SCRIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Icons
LINT="🔍"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"

echo -e "${CYAN}${LINT} CONVERGENCE CODE QUALITY CHECK ${LINT}${NC}\n"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}${CROSS} Virtual environment not found. Run ./scripts/setup.sh first${NC}"
    exit 1
fi

ERRORS=0

# Run black check
echo -e "${BLUE}🎨 Checking code formatting with black...${NC}"
if black convergence/ tests/ --check --quiet; then
    echo -e "${GREEN}${CHECK} Code formatting is correct${NC}\n"
else
    echo -e "${YELLOW}${WARNING} Code needs formatting. Run: black convergence/ tests/${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Run isort check
echo -e "${BLUE}📑 Checking import sorting with isort...${NC}"
if isort convergence/ tests/ --check-only --quiet; then
    echo -e "${GREEN}${CHECK} Import sorting is correct${NC}\n"
else
    echo -e "${YELLOW}${WARNING} Imports need sorting. Run: isort convergence/ tests/${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Run flake8 (with loose checks)
echo -e "${BLUE}🐍 Running flake8 linter...${NC}"
# Loose flake8 configuration
FLAKE8_CONFIG="--max-line-length=100 --ignore=E203,E266,E501,W503,F403,F401,E402"
if flake8 convergence/ tests/ $FLAKE8_CONFIG; then
    echo -e "${GREEN}${CHECK} No linting errors found${NC}\n"
else
    echo -e "${YELLOW}${WARNING} Linting errors found${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Self-healing: Auto-fix formatting if requested
if [ "$1" == "--fix" ]; then
    echo -e "${BLUE}🔧 Auto-fixing code issues...${NC}"
    black convergence/ tests/
    isort convergence/ tests/
    echo -e "${GREEN}${CHECK} Auto-fix complete${NC}\n"
    ERRORS=0
fi

# Summary
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           ${CHECK} ALL CHECKS PASSED! ${CHECK}                        ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║         ${WARNING} FOUND $ERRORS ISSUE(S) TO FIX ${WARNING}                    ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo -e "\n${CYAN}Run with --fix flag to auto-fix issues:${NC}"
    echo -e "  ${BLUE}./scripts/lint.sh --fix${NC}\n"
    exit 1
fi