import io
import random
from typing import Optional, Tuple

from openai import OpenAI

from convergence.core.models import Conversation


def get_random_female_voice_id() -> str:
    """
    Get the female voice ID from the OpenAI API.
    """
    female_voices = ["alloy", "coral", "fable", "nova", "sage"]
    random_voice = random.choice(female_voices)
    return random_voice


def get_random_male_voice_id() -> str:
    """
    Get the male voice ID from the OpenAI API.
    """
    male_voices = ["ash", "ballad", "echo", "onyx", "shimmer"]
    random_voice = random.choice(male_voices)
    return random_voice


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
        print(f"Converting message to audio using voice: {voice_id}")
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
        print("Successfully converted message to audio.")
        return audio_buffer.read(), None
    except Exception as e:
        print(f"Error converting message to audio: {e}")
        return None, str(e)


def conversation_to_audio(
    conversation: Conversation,
    openai_api_key: str,
    voice_id: str,
    model: str = "tts-1",
    instructions: str = "Speak in a cheerful and positive tone.",
) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Convert a conversation to audio and return the audio buffer.
    """
    try:
        openai_api_key = conversation.config.openai_api_key or ""
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

            voice_id = name_to_voice_id[item.name]

            audio_data, error = text_to_audio(
                item.message,
                openai_api_key,
                voice_id=voice_id,
                model=model,
                instructions=instructions,
            )

            if error:
                print(f"Error converting message to audio: {error}")
                return None, error

            audio_segments.append((idx, audio_data))

        # Sort by message index (already in order, but explicit)
        audio_segments.sort(key=lambda x: x[0])

        # Concatenate all audio segments
        net_audio_buffer = io.BytesIO()
        for _, segment in audio_segments:
            if segment:
                net_audio_buffer.write(segment)

        net_audio_buffer.seek(0)
        return net_audio_buffer.read(), None

    except Exception as e:
        print(f"Error converting conversation to audio: {e}")
        return None, str(e)
