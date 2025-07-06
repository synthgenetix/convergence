from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

from convergence.core.models import ConversationConfig, Transcript, TranscriptItem


def generate_transcript(
    config: ConversationConfig, model: str = "gpt-4o-mini"
) -> Tuple[Optional[Transcript], Optional[str]]:
    """
    Generate a transcript from a conversation.
    """
    try:
        openai = OpenAI(api_key=config.openai_api_key)
        vibe = config.vibe
        prompt = config.prompt
        # outline = config.outline
        # outline_source = config.outline_source  # TODO: use this to generate the outline
        duration = config.duration

        # Generate approximately 2-3 exchanges per minute
        exchanges_per_minute = 2
        total_segments = max(duration * exchanges_per_minute, 4)  # At least 4 exchanges
        start_time = datetime.now()
        segment_index = 0
        transcript_items: List[Any] = []

        while segment_index < total_segments:
            try:
                # Space out exchanges evenly across the duration
                seconds_between_exchanges = (duration * 60) / total_segments
                current_index_timestamp = start_time + timedelta(
                    seconds=segment_index * seconds_between_exchanges
                )

                last_five_transcript_items = transcript_items[-5:]
                last_five_transcript_items_str = "\n".join(
                    [
                        f"{item.timestamp} {item.name} {item.message}"
                        for item in last_five_transcript_items
                    ]
                )

                segment_prompt = f"""
                    Generate a transcript item for the segment {segment_index + 1} of {total_segments}.
                    Return ONLY a JSON object in the following format:
                    {{
                        "timestamp": "2025-07-07T09:00:24",
                        "name": "Speaker Name",
                        "gender": "male or female",
                        "role": "Their Role",
                        "message": "What they say in this segment"
                    }}

                    Context:
                    - Vibe: '{vibe}'
                    - Prompt: '{prompt}'
                    - This is part of a conversation between two people
                    - Make the dialogue natural and engaging

                    Last 5 transcript items:
                    '''
                    {last_five_transcript_items_str}
                    '''

                    Generate the next dialogue turn as JSON.
                    """

                if segment_index + 1 == total_segments:
                    segment_prompt += """
                        The last segment should be the end of the conversation.
                        Make sure the end of the conversation is smooth and not abrupt.
                        The transcript item should be in the following format:
                        {{
                            "timestamp": "2025-07-07T09:00:24",
                            "name": "Customer",
                            "gender": "male",
                            "role": "Customer",
                            "message": "What I want is for you to stop wasting my time. This is harassment.",
                        }}
                    """
                # Use chat completion with structured output
                response = openai.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that generates realistic conversation transcripts in JSON format.",
                        },
                        {"role": "user", "content": segment_prompt},
                    ],
                    response_format={"type": "json_object"},
                )

                # Parse the JSON response
                import json

                response_json = (
                    json.loads(response.choices[0].message.content)
                    if response.choices[0].message.content
                    else {}
                )

                # Create TranscriptItem from the response
                transcript_item = TranscriptItem(**response_json)
                transcript_item.timestamp = current_index_timestamp
                transcript_items.append(transcript_item)
                segment_index += 1
            except Exception as e:
                print(f"Error generating transcript: {e}")
                return None, str(e)

        transcript = Transcript(items=transcript_items)

        return transcript, None
    except Exception as e:
        print(f"Error generating transcript: {e}")
        return None, str(e)
