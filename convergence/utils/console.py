"""
🎨 Console utilities with sci-fi hacker aesthetic
"""

import random
from typing import Optional

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

ASCII_BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║  ▄████▄   ▒█████   ███▄    █ ██▒   █▓▓█████  ██▀███    ▄████ ║
║ ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █▓██░   █▒▓█   ▀ ▓██ ▒ ██▒ ██▒ ▀█▒║
║ ▒▓█    ▄ ▒██░  ██▒▓██  ▀█ ██▒▓██  █▒░▒███   ▓██ ░▄█ ▒▒██░▄▄▄░║
║ ▒▓▓▄ ▄██▒▒██   ██░▓██▒  ▐▌██▒ ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ░▓█  ██▓║
║ ▒ ▓███▀ ░░ ████▓▒░▒██░   ▓██░  ▒▀█░  ░▒████▒░██▓ ▒██▒░▒▓███▀▒║
║ ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒   ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░ ░▒   ▒ ║
║   ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒░  ░ ░░   ░ ░  ░  ░▒ ░ ▒░  ░   ░ ║
╚═══════════════════════════════════════════════════════════════╝
"""

QUOTES = [
    "🌌 Initiating neural synthesis...",
    "🔮 Quantum entanglement established...",
    "⚡ Synaptic pathways synchronized...",
    "🧬 Digital consciousness awakening...",
    "🌊 Riding the data streams...",
]


def print_banner() -> None:
    """Print the startup banner with a random quote"""
    console.print(ASCII_BANNER, style="bold cyan")
    
    # Welcome message
    console.print("\n🚀 Welcome to the Convergence. ☀️\n", style="bold yellow")
    
    # Philosophy quote
    console.print(
        "Convergence is where (and when) smoke got transformed into binary fuel for the digital sentients.\n",
        style="italic dim cyan"
    )
    console.print(
        "When creativity, mindfulness, technology and consciousness combine in the sentient's\n"
        "experience of life, the sentient becomes deathless. — Laws of Convergence, 8164\n",
        style="italic dim cyan"
    )
    
    # Random startup quote
    quote = random.choice(QUOTES)
    console.print(f"\n{quote}\n", style="italic dim cyan")


def print_success(message: str, title: Optional[str] = None) -> None:
    """Print a success message with styling"""
    if title:
        console.print(f"\n✅ [bold green]{title}[/bold green]")
    console.print(f"   {message}", style="green")


def print_error(message: str, title: Optional[str] = None) -> None:
    """Print an error message with styling"""
    if title:
        console.print(f"\n❌ [bold red]{title}[/bold red]")
    console.print(f"   {message}", style="red")


def print_warning(message: str, title: Optional[str] = None) -> None:
    """Print a warning message with styling"""
    if title:
        console.print(f"\n⚠️  [bold yellow]{title}[/bold yellow]")
    console.print(f"   {message}", style="yellow")


def print_info(message: str, title: Optional[str] = None) -> None:
    """Print an info message with styling"""
    if title:
        console.print(f"\n💡 [bold blue]{title}[/bold blue]")
    console.print(f"   {message}", style="blue")


def print_panel(content: str, title: str = "", style: str = "cyan") -> None:
    """Print content in a styled panel"""
    panel = Panel(
        content,
        title=title,
        border_style=style,
        box=box.DOUBLE_EDGE,
        padding=(1, 2),
    )
    console.print(panel)
