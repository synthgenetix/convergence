"""
🔐 Environment configuration with self-healing capabilities
"""

import os
from pathlib import Path
from typing import Dict, Optional, Set

from dotenv import load_dotenv

from convergence.utils.console import console, print_error, print_success, print_warning


def find_env_file(env_name: Optional[str] = None) -> Optional[Path]:
    """
    Find the appropriate .env file with fallback strategy
    Priority: .env.{environment} -> .env -> .env.local
    """
    root_dir = Path.cwd()

    # Get environment name from parameter or ENV variable
    environment = env_name or os.getenv("ENVIRONMENT", "").lower()

    # Define search order
    env_files = []
    if environment:
        env_files.append(f".env.{environment}")
    env_files.extend([".env", ".env.local"])

    # Search for env files
    for env_file in env_files:
        env_path = root_dir / env_file
        if env_path.exists():
            return env_path

    return None


def load_environment(env_path: Optional[str] = None) -> Dict[str, str]:
    """
    Load environment variables with self-healing fallback
    """
    loaded_from: Optional[Path] = None

    if env_path:
        # Use specified path
        env_file = Path(env_path)
        if env_file.exists():
            load_dotenv(env_file)
            loaded_from = env_file
        else:
            print_warning(f"Specified env file not found: {env_path}", "Environment")

    if not loaded_from:
        # Use fallback strategy
        fallback_file = find_env_file()
        if fallback_file:
            load_dotenv(fallback_file)
            loaded_from = fallback_file

    if loaded_from:
        print_success(f"Loaded from: {loaded_from}", "Environment")
    else:
        print_warning("No environment file found, using system environment", "Environment")

    # Return current environment
    return dict(os.environ)


def validate_environment(required_vars: Set[str]) -> bool:
    """
    Validate that required environment variables are set
    """
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print_error(
            f"Missing required environment variables: {', '.join(missing_vars)}",
            "Environment Validation Failed",
        )
        return False

    return True


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with optional validation
    """
    value = os.getenv(key, default)

    if required and not value:
        raise ValueError(f"Required environment variable '{key}' is not set")

    return value
