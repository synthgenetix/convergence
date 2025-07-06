#!/bin/bash

# 🔒 CONVERGENCE SECURITY CHECK SCRIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Icons
LOCK="🔒"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
SHIELD="🛡️"

echo -e "${CYAN}${LOCK} CONVERGENCE SECURITY SCAN ${LOCK}${NC}\n"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}${CROSS} Virtual environment not found. Run ./scripts/setup.sh first${NC}"
    exit 1
fi

# Run bandit
echo -e "${BLUE}${SHIELD} Running Bandit security scanner...${NC}"
echo -e "${YELLOW}Note: Skipping assert_used test (B101) for testing code${NC}\n"

# Run bandit with configuration
if bandit -r convergence/ -ll -i -x tests/; then
    echo -e "\n${GREEN}${CHECK} No security issues found${NC}"
    SECURITY_PASSED=true
else
    echo -e "\n${YELLOW}${WARNING} Security scan found potential issues${NC}"
    SECURITY_PASSED=false
fi

# Additional security checks
echo -e "\n${BLUE}🔍 Running additional security checks...${NC}"

# Check for hardcoded secrets
echo -e "  Checking for hardcoded secrets..."
if grep -r "OPENAI_API_KEY\s*=\s*[\"'][^\"']\+[\"']" convergence/ 2>/dev/null; then
    echo -e "  ${RED}${CROSS} Found hardcoded API keys!${NC}"
    SECURITY_PASSED=false
else
    echo -e "  ${GREEN}${CHECK} No hardcoded secrets found${NC}"
fi

# Check for unsafe file operations
echo -e "  Checking for unsafe file operations..."
if grep -r "eval(" convergence/ 2>/dev/null || grep -r "exec(" convergence/ 2>/dev/null; then
    echo -e "  ${RED}${CROSS} Found potentially unsafe operations!${NC}"
    SECURITY_PASSED=false
else
    echo -e "  ${GREEN}${CHECK} No unsafe operations found${NC}"
fi

# Summary
if [ "$SECURITY_PASSED" = true ]; then
    echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         ${CHECK} SECURITY SCAN PASSED! ${CHECK}                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "\n${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║    ${WARNING} SECURITY SCAN FOUND POTENTIAL ISSUES ${WARNING}             ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"
    
    echo -e "\n${CYAN}${SHIELD} Security recommendations:${NC}"
    echo -e "  • Never hardcode API keys or secrets"
    echo -e "  • Use environment variables for sensitive data"
    echo -e "  • Avoid eval() and exec() functions"
    echo -e "  • Validate all user inputs"
    echo -e "  • Use parameterized queries for databases\n"
    
    exit 1
fi