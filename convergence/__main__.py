"""
🚀 CONVERGENCE CLI Entry Point
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.traceback import install

from convergence.ai.text_to_speech import conversation_to_audio
from convergence.ai.transcript_generator import generate_transcript as generate_transcript_ai
from convergence.core.generator import ConversationGenerator
from convergence.core.models import Conversation, ConversationConfig
from convergence.services.outline import OutlineProcessor
from convergence.utils.console import (
    console,
    print_banner,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from convergence.utils.env import load_environment, validate_environment

# Install rich traceback for better error display
install(show_locals=True)


@click.command()
@click.option(
    "--prompt",
    "-p",
    help="🎯 The conversation topic/prompt (required unless using --conversation)",
)
@click.option(
    "--duration",
    "-d",
    type=int,
    default=10,
    help="⏱️  Approximate duration in minutes (1-60)",
)
@click.option(
    "--env",
    "-e",
    type=click.Path(exists=True),
    help="🔐 Path to env file for OPENAI_API_KEY",
)
@click.option(
    "--vibe",
    "-v",
    default="Storytelling and depiction of events",
    help="🎭 The conversation vibe/style",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="💾 Output file path (default: output/convergence_audio_${timestamp}.wav)",
)
@click.option(
    "--outline",
    "-u",
    help="📋 Path to outline file or URL to guide the conversation",
)
@click.option(
    "--conversation",
    "-c",
    type=click.Path(exists=True),
    help="🗣️ Path to JSON file containing a pre-defined conversation",
)
@click.option(
    "--generate-transcript",
    "-gt",
    is_flag=True,
    help="📝 Generate a conversation transcript and save as JSON",
)
def main(
    prompt: Optional[str],
    duration: int,
    env: Optional[str],
    vibe: str,
    output: Optional[str],
    outline: Optional[str],
    conversation: Optional[str],
    generate_transcript: bool,
) -> None:
    """
    🌌 CONVERGENCE - AI-Powered Audio Conversation Generator

    Generate realistic audio conversations between AI personas.
    """
    # Show banner
    print_banner()

    try:
        # Validate inputs
        if not prompt and not conversation and not generate_transcript:
            print_error(
                "Either --prompt, --conversation, or --generate-transcript must be provided",
                "Missing Required Input",
            )
            sys.exit(1)

        if conversation and generate_transcript:
            print_error(
                "Cannot use --conversation and --generate-transcript together", "Invalid Options"
            )
            sys.exit(1)

        if prompt and conversation:
            print_warning(
                "Both --prompt and --conversation provided, using --conversation", "Input Conflict"
            )

        # Load environment
        console.print("\n🔐 [bold cyan]INITIALIZING ENVIRONMENT[/bold cyan]")
        load_environment(env)

        # Validate required environment variables
        if not validate_environment({"OPENAI_API_KEY"}):
            print_error(
                "Please set OPENAI_API_KEY in your environment or .env file", "Configuration Error"
            )
            sys.exit(1)

        # Handle conversation mode
        if conversation:
            console.print("\n🗣️ [bold cyan]LOADING CONVERSATION[/bold cyan]")
            console.print(f"   File: {conversation}")

            # Load and parse JSON
            with open(conversation, "r") as f:
                conversation_data = json.load(f)

            # Process $env.OPENAI_API_KEY substitution
            if "config" in conversation_data and "openai_api_key" in conversation_data["config"]:
                if conversation_data["config"]["openai_api_key"] == "$env.OPENAI_API_KEY":
                    conversation_data["config"]["openai_api_key"] = os.getenv("OPENAI_API_KEY")

            # Create Conversation object
            conversation_obj = Conversation(**conversation_data)

            console.print("   ✅ Conversation loaded successfully")
            console.print(f"   📊 {len(conversation_obj.transcript.items)} transcript items")

            # Use output path from conversation or override
            if output:
                output_path = Path(output)
            else:
                output_path = conversation_obj.config.output_path or Path(
                    f"output/convergence_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                )

            # Generate audio directly from conversation
            console.print("\n🎵 [bold cyan]GENERATING AUDIO FROM CONVERSATION[/bold cyan]")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate audio using TTS
            audio_data, error = conversation_to_audio(
                conversation_obj, conversation_obj.config.openai_api_key or "", "nova"
            )

            if error or not audio_data:
                print_error(
                    f"Audio generation failed: {error or 'No audio data returned'}", "TTS Error"
                )
                sys.exit(1)

            # Write audio to file
            output_path.write_bytes(audio_data)

            print_success(f"Audio saved to: {output_path}", "🎉 Conversation Audio Generated!")
            console.print(f"   Size: {len(audio_data):,} bytes")

            sys.exit(0)

        # Handle transcript generation mode
        if generate_transcript:
            console.print("\n📝 [bold cyan]GENERATING TRANSCRIPT[/bold cyan]")

            # Use defaults if not provided
            if not prompt:
                prompt = "Two friends having a casual conversation about technology"
                console.print(f"   Using default prompt: {prompt}")

            if not vibe:
                vibe = "Casual and friendly"

            # Create configuration for transcript generation
            config = ConversationConfig(
                prompt=prompt,
                duration=duration,
                vibe=vibe,
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                output_path=None,
                outline=None,
                outline_source=None,
            )

            console.print(f"   Prompt: {prompt}")
            console.print(f"   Duration: {duration} minutes")
            console.print(f"   Vibe: {vibe}")

            # Generate transcript
            transcript, error = generate_transcript_ai(config)

            if error or not transcript:
                print_error(
                    f"Transcript generation failed: {error or 'No transcript returned'}",
                    "Generation Error",
                )
                sys.exit(1)

            console.print(f"   ✅ Generated {len(transcript.items)} transcript items")

            # Create conversation object
            conversation_data = {
                "transcript": transcript.model_dump(),
                "config": {
                    "prompt": config.prompt,
                    "duration": config.duration,
                    "vibe": config.vibe,
                    "output_path": str(config.output_path) if config.output_path else None,
                    # Don't include API key in output
                    "openai_api_key": "$env.OPENAI_API_KEY",
                    "outline": config.outline,
                    "outline_source": config.outline_source,
                },
            }

            # Save to JSON file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_path = Path(f"output/conversation_{timestamp}.json")
            json_path.parent.mkdir(parents=True, exist_ok=True)

            with open(json_path, "w") as f:
                json.dump(conversation_data, f, indent=2, default=str)

            print_success(f"Transcript saved to: {json_path}", "🎉 Transcript Generated!")
            console.print(f"   📊 Total items: {len(transcript.items)}")
            console.print(f"   💾 File size: {json_path.stat().st_size:,} bytes")

            # Show sample of generated conversation
            console.print("\n📖 [bold cyan]SAMPLE CONVERSATION[/bold cyan]")
            for item in transcript.items[:3]:
                console.print(f"   [{item.name}]: {item.message[:80]}...")
            if len(transcript.items) > 3:
                console.print(f"   ... and {len(transcript.items) - 3} more items")

            sys.exit(0)

        # Process outline if provided (for regular mode)
        outline_content = None
        outline_source = None
        if outline:
            console.print("\n📋 [bold cyan]PROCESSING OUTLINE[/bold cyan]")
            outline_processor = OutlineProcessor()
            outline_content, outline_error = outline_processor.process_outline(outline)

            if outline_error:
                print_warning(f"Outline processing failed: {outline_error}")
                print_warning("Continuing without outline")
            else:
                outline_source = outline
                console.print("   ✅ Outline processed successfully")

        # Create configuration (for regular mode)
        if output:
            output_path = Path(output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"output/convergence_audio_{timestamp}.wav")

        config = ConversationConfig(
            prompt=prompt or "",
            duration=duration,
            vibe=vibe,
            output_path=output_path,
            outline=outline_content,
            outline_source=outline_source,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Display configuration
        console.print("\n⚡ [bold cyan]CONFIGURATION[/bold cyan]")
        console.print(f"   Prompt: {config.prompt}")
        console.print(f"   Duration: {config.duration} minutes")
        console.print(f"   Vibe: {config.vibe}")
        console.print(f"   Output: {config.output_path}")
        if config.outline:
            console.print(f"   Outline: {config.outline_source} (loaded)")

        # Generate conversation
        console.print("\n🧬 [bold cyan]GENERATING CONVERSATION[/bold cyan]")
        generator = ConversationGenerator(config)

        # Run async generation
        result = asyncio.run(generator.generate())

        # Display result
        if result.success:
            print_success(f"Conversation saved to: {result.output_path}", "🎉 Generation Complete!")
            if result.duration_seconds:
                console.print(f"   Total time: {result.duration_seconds} seconds")
        else:
            print_error(result.error or "Unknown error occurred", "Generation Failed")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n\n⚠️  [yellow]Process interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        print_error(str(e), "Unexpected Error")
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
