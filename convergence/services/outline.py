"""
📝 Outline processing service
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests

from convergence.services.md import convert_to_md
from convergence.utils.console import console, print_error, print_warning


class OutlineProcessor:
    """Service for processing outline files and URLs"""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Convergence/0.1.0"})

    def is_url(self, source: str) -> bool:
        """Check if the source is a URL"""
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def fetch_from_url(self, url: str) -> Tuple[str, Optional[str]]:
        """Fetch content from a URL"""
        try:
            console.print(f"   🌐 Fetching outline from URL: {url}", style="dim")

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            content = response.text
            console.print(f"   ✅ Fetched {len(content)} characters", style="dim green")

            return content, None

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to fetch URL: {str(e)}"
            print_error(error_msg, "Outline Fetch Error")
            return "", error_msg
        except Exception as e:
            error_msg = f"Unexpected error fetching URL: {str(e)}"
            print_error(error_msg, "Outline Error")
            return "", error_msg

    def read_from_file(self, file_path: str) -> Tuple[str, Optional[str]]:
        """Read content from a file"""
        try:
            path = Path(file_path)

            if not path.exists():
                error_msg = f"File not found: {file_path}"
                print_error(error_msg, "Outline Error")
                return "", error_msg

            if not path.is_file():
                error_msg = f"Not a file: {file_path}"
                print_error(error_msg, "Outline Error")
                return "", error_msg

            console.print(f"   📄 Reading outline from file: {file_path}", style="dim")

            # Check if it's a markdown file or needs conversion
            if path.suffix.lower() in [".md", ".txt"]:
                # Direct text read
                content = path.read_text(encoding="utf-8")
                console.print(f"   ✅ Read {len(content)} characters", style="dim green")
                return content, None
            else:
                # Try to convert to markdown
                console.print(f"   🔄 Converting {path.suffix} to markdown...", style="dim")
                content, error = convert_to_md(str(path))

                if error:
                    print_warning(f"Conversion warning: {error}")
                    # Fallback to text read
                    try:
                        content = path.read_text(encoding="utf-8")
                    except Exception:
                        return "", f"Failed to read file: {error}"

                console.print(f"   ✅ Converted to {len(content)} characters", style="dim green")
                return content, None

        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            print_error(error_msg, "Outline Error")
            return "", error_msg

    def process_outline(self, source: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Process an outline from either a URL or file path
        Returns: (content, error)
        """
        if not source:
            return None, None

        source = source.strip()

        # Check if it's a URL
        if self.is_url(source):
            content, error = self.fetch_from_url(source)
        else:
            # Treat as file path
            content, error = self.read_from_file(source)

        if error:
            return None, error

        # Clean and validate content
        if content:
            content = content.strip()
            if len(content) > 50000:  # Limit outline size to 50KB
                print_warning("Outline truncated to 50,000 characters")
                content = content[:50000]

            # Add some formatting
            content = self._format_outline(content)

        return content, None

    def _format_outline(self, content: str) -> str:
        """Format the outline content for better processing"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line:
                # Ensure bullet points are consistent
                if line.startswith(("-", "*", "•")):
                    line = f"• {line[1:].strip()}"
                formatted_lines.append(line)

        return "\n".join(formatted_lines)
