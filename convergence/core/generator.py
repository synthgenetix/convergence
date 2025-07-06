"""
🎭 Conversation Generator with self-healing capabilities
"""

import asyncio
import time
from pathlib import Path
from typing import Optional

from convergence.core.models import ConversationConfig, ConversationResult, Conversation
from convergence.ai.transcript_generator import generate_transcript as generate_transcript_ai
from convergence.ai.text_to_speech import conversation_to_audio
from convergence.utils.console import print_error, print_info, print_success, print_warning


class ConversationGenerator:
    """Main generator for creating AI-powered audio conversations"""

    def __init__(self, config: ConversationConfig):
        self.config = config

    async def generate(self) -> ConversationResult:
        """
        Generate an audio conversation with self-healing fallbacks
        """
        start_time = time.time()

        try:
            # Step 1: Generate transcript
            print_info("🧬 Generating conversation transcript...", "Phase 1")
            transcript = await self._generate_transcript_with_retry()

            if not transcript:
                return ConversationResult(
                    success=False, error="Failed to generate transcript after retries"
                )

            # Step 2: Convert to audio
            print_info("🎵 Converting transcript to audio...", "Phase 2")
            audio_data = await self._convert_to_audio_with_retry(transcript)

            if not audio_data:
                # Fallback: Save transcript only
                print_warning("Audio generation failed, saving transcript only")
                return self._save_transcript_fallback(transcript)

            # Step 3: Save audio file
            print_info("💾 Writing audio to file...", "Phase 3")
            output_path = await self._save_audio_with_retry(audio_data)

            if not output_path:
                return ConversationResult(success=False, error="Failed to save audio file")

            # Calculate duration
            duration_seconds = int(time.time() - start_time)

            print_success(
                f"Audio saved to: {output_path}", "✨ Conversation Generated Successfully!"
            )

            return ConversationResult(
                success=True,
                output_path=output_path,
                duration_seconds=duration_seconds,
                transcript=transcript,
            )

        except Exception as e:
            print_error(f"Unexpected error: {str(e)}", "Generation Failed")
            return ConversationResult(success=False, error=f"Unexpected error: {str(e)}")

    async def _generate_transcript_with_retry(self, max_retries: int = 3):
        """Generate transcript with retry logic"""
        for attempt in range(max_retries):
            try:
                # Use the real AI transcript generator
                transcript, error = await asyncio.to_thread(
                    generate_transcript_ai, self.config
                )
                if error:
                    raise Exception(error)
                if transcript:
                    return transcript
            except Exception as e:
                print_warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2**attempt)  # Exponential backoff
        return None

    async def _convert_to_audio_with_retry(
        self, transcript, max_retries: int = 2
    ) -> Optional[bytes]:
        """Convert transcript to audio with retry logic"""
        for attempt in range(max_retries):
            try:
                # Create a Conversation object from the transcript
                conversation = Conversation(
                    transcript=transcript,
                    config=self.config
                )
                
                # Use the real TTS service
                audio_data, error = await asyncio.to_thread(
                    conversation_to_audio,
                    conversation,
                    self.config.openai_api_key or "",
                    "nova"  # Default voice
                )
                
                if error:
                    raise Exception(error)
                if audio_data:
                    return audio_data
            except Exception as e:
                print_warning(f"Audio conversion attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2**attempt)
        return None

    async def _save_audio_with_retry(
        self, audio_data: bytes, max_retries: int = 2
    ) -> Optional[Path]:
        """Save audio to file with retry logic"""
        # Generate default path if not provided
        if not self.config.output_path:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.config.output_path = Path(f"output/convergence_audio_{timestamp}.wav")

        # Ensure output directory exists
        self.config.output_path.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(max_retries):
            try:
                # Write the audio data directly
                self.config.output_path.write_bytes(audio_data)
                return self.config.output_path
            except Exception as e:
                print_warning(f"Save attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
        return None

    def _save_transcript_fallback(self, transcript) -> ConversationResult:
        """Fallback to save transcript as JSON file"""
        try:
            # Generate default path if not provided
            if not self.config.output_path:
                from datetime import datetime

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.config.output_path = Path(f"output/convergence_audio_{timestamp}.wav")

            transcript_path = self.config.output_path.with_suffix(".json")
            transcript_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save as JSON
            import json
            conversation_data = {
                "transcript": transcript.model_dump(),
                "config": {
                    "prompt": self.config.prompt,
                    "duration": self.config.duration,
                    "vibe": self.config.vibe,
                    "output_path": str(self.config.output_path) if self.config.output_path else None,
                    "openai_api_key": "$env.OPENAI_API_KEY",
                    "outline": self.config.outline,
                    "outline_source": self.config.outline_source,
                },
            }
            
            with open(transcript_path, "w") as f:
                json.dump(conversation_data, f, indent=2, default=str)

            return ConversationResult(
                success=True,
                output_path=transcript_path,
                transcript=transcript,
                error="Audio generation failed, transcript saved as JSON",
            )
        except Exception as e:
            return ConversationResult(
                success=False, transcript=transcript, error=f"Failed to save transcript: {str(e)}"
            )
