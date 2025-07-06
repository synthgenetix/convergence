import io
import random
from typing import Optional, Tuple

from openai import OpenAI

from convergence.core.models import Conversation


def get_random_female_voice_id() -> str:
    """
    Get a female-presenting voice ID from the OpenAI API.
    """
    female_voices = ["coral", "fable", "nova", "sage", "shimmer"]
    return random.choice(female_voices)


def get_random_male_voice_id() -> str:
    """
    Get a male-presenting voice ID from the OpenAI API.
    """
    male_voices = ["alloy", "ash", "ballad", "echo", "onyx"]
    return random.choice(male_voices)


def text_to_audio(
    message: str,
    openai_api_key: str,
    voice_id: str,
    model: str = "tts-1",
    instructions: str = "Speak in a cheerful and positive tone.",
) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Convert a message to audio and return the audio buffer.
    Returns:
        Tuple[Optional[bytes], Optional[str]]: (audio_buffer, error_message_if_any)
    """
    try:
        openai = OpenAI(api_key=openai_api_key)
        audio_buffer = io.BytesIO()

        # Create speech response
        response = openai.audio.speech.create(
            model=model, voice=voice_id, input=message, response_format="wav"
        )

        # Write the response content to buffer
        for chunk in response.iter_bytes():
            audio_buffer.write(chunk)

        audio_buffer.seek(0)
        return audio_buffer.read(), None
    except Exception as e:
        print(f"Error converting message to audio: {e}")
        return None, str(e)


def conversation_to_audio(
    conversation: Conversation,
    openai_api_key: str,
    voice_id: str,  # Currently unused - voices are assigned randomly per speaker
    model: str = "tts-1",
    instructions: str = "Speak in a cheerful and positive tone.",
) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Convert a conversation to audio and return the audio buffer.
    """
    try:
        # Use the provided API key, fall back to conversation config if not provided
        api_key = openai_api_key or conversation.config.openai_api_key or ""
        transcript = conversation.transcript

        name_to_voice_id = {}
        audio_segments = []

        for idx, item in enumerate(transcript.items):
            # Assign a voice ID per speaker
            if item.name not in name_to_voice_id:
                if item.gender == "female":
                    name_to_voice_id[item.name] = get_random_female_voice_id()
                else:
                    name_to_voice_id[item.name] = get_random_male_voice_id()

            assigned_voice_id = name_to_voice_id[item.name]

            print(f"Converting message to audio for segment {idx} of {len(transcript.items)}.")
            audio_data, error = text_to_audio(
                item.message,
                api_key,
                voice_id=assigned_voice_id,
                model=model,
                instructions=instructions,
            )

            if error:
                print(f"Error converting message to audio: {error}")
                return None, error

            audio_segments.append((idx, audio_data))

        print(f"{len(audio_segments)} audio segments generated.")

        # Sort by message index (already in order, but explicit)
        audio_segments.sort(key=lambda x: x[0])

        # Concatenate all audio segments
        # For WAV files, we need to strip headers from all but the first segment
        net_audio_buffer = io.BytesIO()

        for idx, (_, segment) in enumerate(audio_segments):
            if segment:
                if idx == 0:
                    # Keep the full WAV file for the first segment
                    net_audio_buffer.write(segment)
                else:
                    # Skip WAV header (44 bytes) for subsequent segments
                    # Only if it's a WAV file (starts with RIFF)
                    if segment[:4] == b"RIFF":
                        net_audio_buffer.write(segment[44:])
                    else:
                        net_audio_buffer.write(segment)

        net_audio_buffer.seek(0)
        audio_bytes = net_audio_buffer.read()

        # Update WAV header with correct file size if it's a WAV file
        if audio_bytes[:4] == b"RIFF":
            audio_array = bytearray(audio_bytes)
            # Update file size (total size - 8)
            file_size = len(audio_array) - 8
            audio_array[4:8] = file_size.to_bytes(4, "little")
            # Update data chunk size (total size - 44)
            data_size = len(audio_array) - 44
            audio_array[40:44] = data_size.to_bytes(4, "little")
            audio_bytes = bytes(audio_array)

        return audio_bytes, None

    except Exception as e:
        print(f"Error converting conversation to audio: {e}")
        return None, str(e)
