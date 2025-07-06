"""
📊 Authentication data models
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class APIKey(BaseModel):
    """API Key model from Google Sheets"""

    api_key: str = Field(..., description="The API key")
    client_name: str = Field(..., description="Name of the client")
    created_at: datetime = Field(..., description="Creation date")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    is_active: bool = Field(True, description="Whether the key is active")
    rate_limit: Optional[int] = Field(None, description="Requests per hour limit")

    def is_valid(self) -> bool:
        """Check if the API key is currently valid"""
        if not self.is_active:
            return False

        if self.expires_at and datetime.now() > self.expires_at:
            return False

        return True

    class Config:
        json_schema_extra = {
            "example": {
                "api_key": "sk-convergence-abc123xyz",
                "client_name": "Acme Corp",
                "created_at": "2024-01-01T00:00:00",
                "expires_at": "2024-12-31T23:59:59",
                "is_active": True,
                "rate_limit": 1000,
            }
        }
