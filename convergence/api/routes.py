"""
🛣️ API Routes for Convergence
"""

import os
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from convergence.core.generator import ConversationGenerator
from convergence.core.models import ConversationConfig, ConversationResult
from convergence.services.outline import OutlineProcessor
from convergence.utils.console import console, print_warning

router = APIRouter()


class GenerateAudioRequest(BaseModel):
    """Request model for audio generation"""

    prompt: str = Field(..., description="The conversation topic/prompt")
    duration: int = Field(10, ge=1, le=60, description="Duration in minutes (1-60)")
    vibe: str = Field(
        "Storytelling and depiction of events", description="The conversation vibe/style"
    )
    outline_url: Optional[str] = Field(
        None, description="URL to outline document (API only accepts URLs, not file paths)"
    )

    @field_validator("outline_url")
    @classmethod
    def validate_outline_url(cls, v: Optional[str]) -> Optional[str]:
        if v:
            # Basic URL validation
            if not (v.startswith("http://") or v.startswith("https://")):
                raise ValueError("Outline must be a valid HTTP/HTTPS URL")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Two friends discussing the latest AI developments",
                "duration": 10,
                "vibe": "Enthusiastic and technical",
                "outline_url": "https://example.com/conversation-outline.md",
            }
        }


class GenerateAudioResponse(BaseModel):
    """Response model for audio generation"""

    success: bool
    output_path: str
    duration_seconds: int
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "output_path": "output/convergence_audio_20240101_120000.wav",
                "duration_seconds": 600,
                "message": "Audio conversation generated successfully",
            }
        }


@router.post(
    "/convergence/generate-audio",
    response_model=GenerateAudioResponse,
    tags=["Convergence"],
    summary="Generate an audio conversation",
    description="Generate an AI-powered audio conversation based on the provided prompt and parameters",
)
async def generate_audio(
    request: GenerateAudioRequest, background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Generate an audio conversation

    This endpoint creates an AI-generated conversation between two personas
    based on the provided prompt, duration, and vibe.
    """
    console.print("\n📡 [bold blue]API REQUEST[/bold blue]")
    console.print(f"   Prompt: {request.prompt}")
    console.print(f"   Duration: {request.duration} minutes")
    console.print(f"   Vibe: {request.vibe}")
    if request.outline_url:
        console.print(f"   Outline URL: {request.outline_url}")

    try:
        # Process outline if provided
        outline_content = None
        outline_source = None
        if request.outline_url:
            console.print("\n📋 Processing outline from URL...")
            outline_processor = OutlineProcessor()
            outline_content, outline_error = outline_processor.process_outline(request.outline_url)

            if outline_error:
                print_warning(f"Outline processing failed: {outline_error}")
                print_warning("Continuing without outline")
            else:
                outline_source = request.outline_url
                console.print("   ✅ Outline processed successfully")

        # Create configuration
        config = ConversationConfig(
            prompt=request.prompt,
            duration=request.duration,
            vibe=request.vibe,
            outline=outline_content,
            outline_source=outline_source,
            output_path=None,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Generate conversation
        generator = ConversationGenerator(config)
        result: ConversationResult = await generator.generate()

        if result.success:
            console.print("\n✅ [bold green]REQUEST COMPLETED[/bold green]")
            return {
                "success": True,
                "output_path": str(result.output_path),
                "duration_seconds": result.duration_seconds or 0,
                "message": "Audio conversation generated successfully",
            }
        else:
            console.print("\n❌ [bold red]REQUEST FAILED[/bold red]")
            raise HTTPException(
                status_code=500, detail=result.error or "Failed to generate audio conversation"
            )

    except Exception as e:
        console.print("\n❌ [bold red]REQUEST ERROR[/bold red]")
        console.print(f"   Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/convergence/download/{filename}",
    tags=["Convergence"],
    summary="Download generated audio file",
    description="Download a previously generated audio conversation file",
)
async def download_audio(filename: str) -> FileResponse:
    """
    Download a generated audio file

    Provide the filename returned from the generate-audio endpoint
    to download the audio file.
    """
    file_path = Path("output") / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail=f"Invalid file: {filename}")

    # Security check: ensure file is in output directory
    try:
        file_path.resolve().relative_to(Path("output").resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")

    return FileResponse(path=file_path, media_type="audio/wav", filename=filename)
