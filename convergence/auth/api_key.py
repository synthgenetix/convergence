"""
🔑 API Key authentication handler
"""

import os
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, Optional, cast

from convergence.auth.google_sheets import get_sheets_client
from convergence.auth.models import APIKey
from convergence.utils.console import console


class APIKeyAuth:
    """API Key authentication handler with caching"""

    def __init__(self) -> None:
        self.sheets_client = get_sheets_client()
        self.cache_duration = int(os.getenv("API_KEY_CACHE_DURATION", "300"))  # 5 minutes
        self._cache: Dict[str, Dict] = {}

    def _get_cache_key(self, api_key: str) -> str:
        """Generate cache key for API key"""
        return f"api_key:{api_key}"

    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        if "expires_at" not in cache_entry:
            return False
        return bool(datetime.now() < cache_entry["expires_at"])

    @lru_cache(maxsize=128)
    def validate_api_key(self, api_key: str) -> Optional[APIKey]:
        """
        Validate API key with caching
        Returns the APIKey object if valid, None otherwise
        """
        # Check cache first
        cache_key = self._get_cache_key(api_key)

        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if self._is_cache_valid(cache_entry):
                console.print("   🚀 API key validated from cache", style="dim green")
                return cast(Optional[APIKey], cache_entry.get("api_key_obj"))

        # Fetch from Google Sheets
        console.print("   📊 Validating API key from Google Sheets", style="dim")

        api_key_obj = self.sheets_client.get_api_key(api_key)

        if api_key_obj and api_key_obj.is_valid():
            # Cache the result
            self._cache[cache_key] = {
                "api_key_obj": api_key_obj,
                "expires_at": datetime.now() + timedelta(seconds=self.cache_duration),
            }
            console.print(
                f"   ✅ API key validated for: {api_key_obj.client_name}", style="dim green"
            )
            return api_key_obj

        # Cache negative result too (to avoid repeated lookups)
        self._cache[cache_key] = {
            "api_key_obj": None,
            "expires_at": datetime.now() + timedelta(seconds=60),  # Cache failures for 1 minute
        }

        return None

    def extract_api_key(self, authorization: Optional[str]) -> Optional[str]:
        """Extract API key from Authorization header"""
        if not authorization:
            return None

        # Support both "Bearer" and "ApiKey" schemes
        parts = authorization.split()
        if len(parts) != 2:
            return None

        scheme, token = parts
        if scheme.lower() in ["bearer", "apikey"]:
            return token

        return None

    def clear_cache(self, api_key: Optional[str] = None) -> None:
        """Clear cache for a specific API key or all keys"""
        if api_key:
            cache_key = self._get_cache_key(api_key)
            self._cache.pop(cache_key, None)
            self.validate_api_key.cache_clear()
        else:
            self._cache.clear()
            self.validate_api_key.cache_clear()

    def get_rate_limit(self, api_key: str) -> Optional[int]:
        """Get rate limit for an API key"""
        api_key_obj = self.validate_api_key(api_key)
        if api_key_obj:
            return api_key_obj.rate_limit
        return None


# Global instance
_api_key_auth: Optional[APIKeyAuth] = None


def get_api_key_auth() -> APIKeyAuth:
    """Get or create the global API key auth handler"""
    global _api_key_auth
    if _api_key_auth is None:
        _api_key_auth = APIKeyAuth()
    return _api_key_auth
