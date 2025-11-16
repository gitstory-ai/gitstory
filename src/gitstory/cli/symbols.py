"""Symbol constants with automatic ASCII fallback for Windows compatibility.

This module provides Unicode symbols (checkmarks, icons, etc.) with automatic
fallback to ASCII equivalents when the console doesn't support UTF-8 encoding.

Based on Rich library's encoding detection approach:
- Modern terminals (UTF-8): Use Unicode symbols (✓, ✗, ℹ, ⚠)
- Legacy Windows/ASCII: Use ASCII equivalents ([OK], [X], [i], [!])

Example:
    >>> from gitstory.cli.symbols import get_symbols
    >>> symbols = get_symbols()
    >>> print(f"{symbols.SUCCESS} Task complete")
    ✓ Task complete  # On UTF-8 terminals
    [OK] Task complete  # On ASCII/Windows terminals
"""

import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass(frozen=True)
class Symbols:
    """Symbol constants for CLI output.

    Attributes:
        SUCCESS: Success indicator (✓ or [OK])
        ERROR: Error indicator (✗ or [X])
        INFO: Info indicator (ℹ or [i])
        WARNING: Warning indicator (⚠ or [!])
        DEBUG: Debug indicator (• or [*])
        ARROW_RIGHT: Right arrow (→ or ->)
        BULLET: Bullet point (• or *)
    """

    SUCCESS: str
    ERROR: str
    INFO: str
    WARNING: str
    DEBUG: str
    ARROW_RIGHT: str
    BULLET: str


# Unicode symbols (for UTF-8 terminals)
UNICODE_SYMBOLS = Symbols(
    SUCCESS="✓",
    ERROR="✗",
    INFO="ℹ",
    WARNING="⚠",
    DEBUG="•",
    ARROW_RIGHT="→",
    BULLET="•",
)

# ASCII-safe fallbacks (for Windows cp1252, ASCII terminals)
ASCII_SYMBOLS = Symbols(
    SUCCESS="[OK]",
    ERROR="[X]",
    INFO="[i]",
    WARNING="[!]",
    DEBUG="[*]",
    ARROW_RIGHT="->",
    BULLET="*",
)


def _supports_unicode(file: TextIO = sys.stdout) -> bool:
    """Detect if the output stream supports Unicode.

    Uses Rich's approach: Check if encoding starts with 'utf'.
    This covers utf-8, utf-16, utf-32, etc.

    Args:
        file: Output stream to check (default: sys.stdout)

    Returns:
        True if Unicode is supported, False otherwise

    Example:
        >>> _supports_unicode()  # On modern terminal
        True
        >>> # On Windows cmd.exe with cp1252
        False
    """
    encoding = getattr(file, "encoding", None)
    if encoding is None:
        # No encoding attribute - assume UTF-8 (safest default)
        return True

    # Normalize encoding name (lowercased)
    encoding_lower = encoding.lower()

    # Check for UTF encodings (utf-8, utf-16, utf-32, etc.)
    if encoding_lower.startswith("utf"):
        return True

    # Known ASCII-only encodings that can't handle Unicode symbols
    ascii_only_encodings = {
        "ascii",
        "cp1252",  # Windows Western Europe
        "cp437",  # DOS/OEM US
        "cp850",  # DOS/OEM Western Europe
        "latin-1",
        "iso-8859-1",
    }

    return encoding_lower not in ascii_only_encodings


def get_symbols(file: TextIO = sys.stdout, force_ascii: bool = False) -> Symbols:
    """Get appropriate symbols for the current terminal.

    Auto-detects terminal capabilities and returns either Unicode or ASCII symbols.
    Follows Rich library's encoding detection approach.

    Args:
        file: Output stream to check encoding (default: sys.stdout)
        force_ascii: If True, always use ASCII symbols (for testing)

    Returns:
        Symbols instance with appropriate glyphs for the terminal

    Example:
        >>> # In CLI code
        >>> symbols = get_symbols()
        >>> print(f"{symbols.SUCCESS} Done")

        >>> # Force ASCII (useful for testing or CI)
        >>> symbols = get_symbols(force_ascii=True)
        >>> assert symbols.SUCCESS == "[OK]"
    """
    if force_ascii or not _supports_unicode(file):
        return ASCII_SYMBOLS
    return UNICODE_SYMBOLS


# Export symbols for convenience
__all__ = ["Symbols", "get_symbols", "UNICODE_SYMBOLS", "ASCII_SYMBOLS"]
