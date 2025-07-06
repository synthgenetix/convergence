"""
🛡️ Authentication middleware for FastAPI
"""

from typing import Any, Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from convergence.auth.api_key import get_api_key_auth
from convergence.utils.console import console


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Middleware to validate API keys on protected endpoints"""

    def __init__(self, app: ASGIApp, auth_enabled: bool = True):
        super().__init__(app)
        self.auth_enabled = auth_enabled
        self.api_key_auth = get_api_key_auth()

        # Endpoints that don't require authentication
        self.public_endpoints = {"/health", "/docs", "/openapi.json", "/redoc", "/favicon.ico"}

        # Endpoints that require authentication
        self.protected_prefixes = ["/convergence/"]

    def _is_protected_endpoint(self, path: str) -> bool:
        """Check if an endpoint requires authentication"""
        # Public endpoints don't need auth
        if path in self.public_endpoints:
            return False

        # Check if path starts with any protected prefix
        for prefix in self.protected_prefixes:
            if path.startswith(prefix):
                return True

        return False

    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        """Process the request and validate API key if needed"""

        # Skip auth if disabled
        if not self.auth_enabled:
            return await call_next(request)

        # Check if endpoint needs protection
        if not self._is_protected_endpoint(request.url.path):
            return await call_next(request)

        # Extract API key from header
        authorization = request.headers.get("Authorization")
        api_key = self.api_key_auth.extract_api_key(authorization)

        if not api_key:
            console.print(f"   ❌ Missing API key for: {request.url.path}", style="red dim")
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Missing API key",
                    "detail": "Please provide an API key in the Authorization header",
                    "example": "Authorization: Bearer your-api-key",
                },
            )

        # Validate API key
        api_key_obj = self.api_key_auth.validate_api_key(api_key)

        if not api_key_obj:
            console.print(f"   ❌ Invalid API key attempted: {api_key[:10]}...", style="red dim")
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Invalid API key",
                    "detail": "The provided API key is invalid or expired",
                },
            )

        # Add API key info to request state
        request.state.api_key = api_key_obj
        request.state.client_name = api_key_obj.client_name

        # Log successful auth
        console.print(
            f"   🔐 Authenticated request from: {api_key_obj.client_name}", style="green dim"
        )

        # Continue with the request
        response = await call_next(request)

        # Add client info to response headers
        response.headers["X-Client-Name"] = api_key_obj.client_name

        return response
