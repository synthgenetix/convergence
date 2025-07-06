"""
📊 Data models for Convergence
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ConversationConfig(BaseModel):
    """Configuration for generating audio conversations"""

    prompt: str = Field(default="", description="The conversation topic/prompt")
    duration: int = Field(10, ge=1, le=60, description="Duration in minutes (1-60)")
    vibe: str = Field("NA", description="The conversation vibe/style")
    output_path: Optional[Path] = Field(None, description="Output file path")
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key")
    outline: Optional[str] = Field(None, description="Outline content to guide the conversation")
    outline_source: Optional[str] = Field(None, description="Source of the outline (file/url)")

    @field_validator("output_path", mode="before")
    @classmethod
    def validate_output_path(cls, v: Optional[str]) -> Optional[Path]:
        if v:
            return Path(v)
        # Return None - default path will be generated when needed
        return None

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Two friends discussing the latest AI developments",
                "duration": 10,
                "vibe": "Enthusiastic and technical",
                "output_path": "output/ai_discussion.wav",
                "outline": "1. Introduction to AI\n2. Recent breakthroughs\n3. Future implications",
            }
        }


class TranscriptItem(BaseModel):
    """Item in the transcript"""

    name: str = Field(..., description="Name of the speaker.")
    gender: str = Field(..., description="Gender of the speaker.")
    role: str = Field(..., description="Role of the speaker.")
    message: str = Field(..., description="Message of the speaker.")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the speaker.")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "role": "Speaker",
                "message": "Hello, how are you?",
                "timestamp": "2021-01-01 12:00:00",
            }
        }


class Transcript(BaseModel):
    """Transcript of the conversation"""

    items: List[TranscriptItem] = Field(..., description="List of transcript items")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "name": "John Doe",
                        "role": "Speaker",
                        "message": "Hello, how are you?",
                        "timestamp": "2021-01-01 12:00:00",
                    },
                    {
                        "name": "Jane Doe",
                        "role": "Listener",
                        "message": "I'm good, thank you!",
                        "timestamp": "2021-01-01 12:01:00",
                    },
                ]
            }
        }


class ConversationResult(BaseModel):
    """Result of conversation generation"""

    success: bool = Field(default=False, description="Whether generation was successful")
    output_path: Optional[Path] = Field(default=None, description="Path to generated audio file")
    duration_seconds: Optional[int] = Field(default=None, description="Actual duration in seconds")
    transcript: Optional[Transcript] = Field(default=None, description="Generated conversation transcript")
    error: Optional[str] = Field(default=None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "output_path": "output/convergence_audio_20240101_120000.wav",
                "duration_seconds": 600,
                "transcript": "Person A: Hey, did you hear about...",
                "error": None,
            }
        }


class Conversation(BaseModel):
    """Conversation"""

    transcript: Transcript = Field(..., description="Transcript of the conversation")
    config: ConversationConfig = Field(..., description="Configuration of the conversation")
