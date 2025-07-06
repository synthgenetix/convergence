"""
🌌 CONVERGENCE - AI Audio Conversation Generator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

__version__ = "0.1.0"
__author__ = "Convergence Labs"

from convergence.core.generator import ConversationGenerator
from convergence.core.models import ConversationConfig

__all__ = ["ConversationGenerator", "ConversationConfig"]
