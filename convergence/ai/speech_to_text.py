from typing import Optional, Tuple

from openai import OpenAI

from convergence.core.models import Conversation


def audio_to_transcript(
    conversation: Conversation, audio_path: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert a conversation to audio and return the transcript.
    """
    try:
        text = ""
        openai = OpenAI(api_key=conversation.config.openai_api_key)
        print(f"Converting audio at {audio_path} to transcript.")

        with open(audio_path, "rb") as f:
            transcription = openai.audio.transcriptions.create(model="gpt-4o-transcribe", file=f)
            text = transcription.text

        print(f"Generated transcript of {len(text)} characters.")
        return text, None
    except Exception as e:
        print(f"Error converting audio to transcript: {e}.")
        return None, str(e)
