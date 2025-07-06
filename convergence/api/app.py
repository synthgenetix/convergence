"""
🚀 FastAPI application for Convergence
"""

import os
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from convergence.api.routes import router
from convergence.auth.google_sheets import get_sheets_client
from convergence.auth.middleware import APIKeyMiddleware
from convergence.utils.console import console, print_banner, print_warning
from convergence.utils.env import load_environment, validate_environment


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Manage application lifecycle"""
    # Startup
    print_banner()
    console.print("\n🌐 [bold cyan]CONVERGENCE API STARTING[/bold cyan]")

    # Load environment
    environment = os.getenv("ENVIRONMENT", "development")
    console.print(f"   Environment: {environment}")

    load_environment()

    # Validate required environment variables
    if not validate_environment({"OPENAI_API_KEY"}):
        console.print("\n❌ [bold red]STARTUP FAILED[/bold red]")
        console.print("   Missing required environment variables")
        raise RuntimeError("Missing required environment variables")

    # Check authentication configuration
    auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    console.print(f"   Authentication: {'Enabled' if auth_enabled else 'Disabled'}")

    if auth_enabled:
        # Check if Google credentials are available
        google_creds = os.getenv("GOOGLE_CREDENTIALS_PATH")
        google_sheet_id = os.getenv("GOOGLE_SHEET_ID")

        if google_creds and google_sheet_id:
            # Try to initialize Google Sheets client
            sheets_client = get_sheets_client()
            if sheets_client.initialize():
                console.print(
                    "   🔐 [bold green]Authentication configured with Google Sheets[/bold green]"
                )
            else:
                print_warning(
                    "Failed to initialize Google Sheets client", "⚠️  AUTHENTICATION WARNING"
                )
                console.print(
                    "   🔓 [bold yellow]Server starting in UNAUTHENTICATED mode[/bold yellow]"
                )
                console.print("   Please check your Google credentials configuration")
        else:
            print_warning(
                "Authentication enabled but Google credentials not configured",
                "⚠️  AUTHENTICATION WARNING",
            )
            console.print(
                "   🔓 [bold yellow]Server starting in UNAUTHENTICATED mode[/bold yellow]"
            )
            console.print("   Required environment variables:")
            console.print("     - GOOGLE_CREDENTIALS_PATH: Path to service account JSON")
            console.print("     - GOOGLE_SHEET_ID: Google Sheet ID containing API keys")
            console.print("     - GOOGLE_SHEET_NAME: Sheet name (default: API_Keys)")

    console.print("\n✅ [bold green]API READY[/bold green]")
    console.print("   Listening for requests...\n")

    yield

    # Shutdown
    console.print("\n👋 [bold yellow]CONVERGENCE API SHUTTING DOWN[/bold yellow]")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="🌌 Convergence API",
        description="AI-Powered Audio Conversation Generator",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Check if authentication is enabled
    auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() == "true"

    # Add API Key middleware if authentication is enabled
    if auth_enabled:
        app.add_middleware(APIKeyMiddleware, auth_enabled=True)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router)

    # Health check endpoint
    @app.get("/health", tags=["Health"])  # type: ignore[misc]
    async def health_check() -> Dict[str, str]:
        """Check if the API is running"""
        auth_status = "enabled" if auth_enabled else "disabled"
        return {
            "status": "healthy",
            "service": "convergence-api",
            "version": "0.1.0",
            "auth": auth_status,
        }

    # Auth status endpoint
    @app.get("/auth/status", tags=["Authentication"])  # type: ignore[misc]
    async def auth_status() -> Dict[str, Any]:
        """Check authentication configuration status"""
        auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() == "true"

        if not auth_enabled:
            return {"auth_enabled": False, "message": "Authentication is disabled"}

        # Check Google Sheets configuration
        google_configured = bool(
            os.getenv("GOOGLE_CREDENTIALS_PATH") and os.getenv("GOOGLE_SHEET_ID")
        )

        sheets_client = get_sheets_client()
        sheets_initialized = sheets_client._initialized

        return {
            "auth_enabled": True,
            "google_sheets_configured": google_configured,
            "google_sheets_connected": sheets_initialized,
            "cache_duration": int(os.getenv("API_KEY_CACHE_DURATION", "300")),
            "sheet_name": os.getenv("GOOGLE_SHEET_NAME", "API_Keys"),
        }

    # Custom exception handler
    @app.exception_handler(HTTPException)  # type: ignore[misc]
    async def http_exception_handler(request: Any, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions with custom formatting"""
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "status_code": exc.status_code, "path": str(request.url)},
        )

    return app


# Create app instance
app = create_app()
