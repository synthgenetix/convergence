#!/bin/bash

# 🔤 CONVERGENCE TYPE CHECK SCRIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Icons
TYPE="🔤"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"

echo -e "${CYAN}${TYPE} CONVERGENCE TYPE CHECKING ${TYPE}${NC}\n"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}${CROSS} Virtual environment not found. Run ./scripts/setup.sh first${NC}"
    exit 1
fi

# Run mypy
echo -e "${BLUE}🔍 Running mypy type checker...${NC}"
echo -e "${YELLOW}Note: Using relaxed type checking for better compatibility${NC}\n"

# Relaxed mypy configuration for loose type checking
MYPY_FLAGS="--ignore-missing-imports --no-strict-optional --allow-untyped-defs --allow-untyped-calls"

if mypy convergence/ $MYPY_FLAGS; then
    echo -e "\n${GREEN}${CHECK} No type errors found${NC}"
    EXIT_CODE=0
else
    echo -e "\n${YELLOW}${WARNING} Type checking found some issues${NC}"
    EXIT_CODE=1
fi

# Self-healing suggestions
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "\n${CYAN}💡 Self-healing suggestions:${NC}"
    echo -e "  • Add type hints to function signatures"
    echo -e "  • Import types from typing module"
    echo -e "  • Use Optional[] for nullable parameters"
    echo -e "  • Consider using Protocol for duck typing"
    
    echo -e "\n${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║      ${WARNING} TYPE CHECKING COMPLETED WITH WARNINGS ${WARNING}          ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         ${CHECK} TYPE CHECKING PASSED! ${CHECK}                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
fi

exit $EXIT_CODE