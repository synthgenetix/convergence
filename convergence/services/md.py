from typing import Optional, Tuple

from markitdown import MarkItDown


def convert_to_md(file_path: str) -> Tuple[str, Optional[str]]:
    """
    Convert a file to Markdown.
    """
    try:
        print(f"Converting {file_path} to Markdown.")
        md = MarkItDown(enable_plugins=False)
        result = md.convert(file_path)
        print(f"Converted {file_path} to Markdown.")
        return result.text_content, None
    except Exception as e:
        print(f"Error converting {file_path} to Markdown: {e}.")
        return "", str(e)
