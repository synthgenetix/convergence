"""
📝 Transcript generation service (stub implementation)
"""

import asyncio
import random
from typing import Optional

from convergence.utils.console import console


class TranscriptService:
    """Service for generating conversation transcripts"""

    def __init__(self) -> None:
        self.personas = [
            {"name": "Alex", "style": "tech enthusiast"},
            {"name": "Sam", "style": "curious learner"},
        ]

    async def generate(
        self, prompt: str, duration: int, vibe: str, outline: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a conversation transcript (stub implementation)
        """
        console.print(f"   📡 Processing prompt: {prompt}", style="dim")
        console.print(f"   ⏱️  Target duration: {duration} minutes", style="dim")
        console.print(f"   🎭 Vibe: {vibe}", style="dim")
        if outline:
            console.print("   📋 Using outline guidance", style="dim")

        # Simulate processing time
        await asyncio.sleep(random.uniform(1.0, 2.0))

        # Generate dummy transcript
        if outline:
            # Extract key points from outline
            outline_points = [line.strip() for line in outline.split("\n") if line.strip()]
            opening_line = f"Looking at the outline about {prompt}"
        else:
            outline_points = []
            opening_line = f"I've been thinking about {prompt}"

        transcript_lines = [
            f"{self.personas[0]['name']}: Hey! {opening_line}.",
            f"{self.personas[1]['name']}: Oh really? That sounds interesting! Tell me more.",
            f"{self.personas[0]['name']}: Well, you know how {vibe.lower()} can really change perspectives?",
            f"{self.personas[1]['name']}: Absolutely! I was just reading about that yesterday.",
        ]

        # If we have outline points, incorporate them
        if outline_points:
            transcript_lines.extend(
                [
                    f"{self.personas[0]['name']}: According to the outline, we should cover {len(outline_points)} key areas.",
                    f"{self.personas[1]['name']}: Great! Let's go through them systematically.",
                ]
            )
        else:
            transcript_lines.extend(
                [
                    f"{self.personas[0]['name']}: It's fascinating how technology is evolving in this space.",
                    f"{self.personas[1]['name']}: Right? The implications are mind-blowing.",
                ]
            )

        # Add more lines based on duration
        base_lines = len(transcript_lines)
        lines_per_minute = 20  # Approximate conversation pace
        total_lines = min(lines_per_minute * duration, 300)  # Cap at 300 lines

        # Use outline points as topics if available, otherwise use defaults
        if outline_points and len(outline_points) > 2:
            topics = outline_points[:10]  # Limit to first 10 points
        else:
            topics = [
                "the future implications",
                "the technical challenges",
                "the social impact",
                "the ethical considerations",
                "the practical applications",
            ]

        for i in range(base_lines, total_lines):
            speaker = self.personas[i % 2]
            topic = random.choice(topics)

            responses = [
                f"That's a great point about {topic}.",
                f"I hadn't considered {topic} from that angle.",
                f"What do you think about {topic}?",
                f"The way {topic} intersects with this is fascinating.",
                f"Let me share my thoughts on {topic}.",
            ]

            line = f"{speaker['name']}: {random.choice(responses)}"
            transcript_lines.append(line)

        transcript = "\n".join(transcript_lines)
        console.print(
            f"   ✅ Generated {len(transcript_lines)} lines of dialogue", style="dim green"
        )

        return transcript
