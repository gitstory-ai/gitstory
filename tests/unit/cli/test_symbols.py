"""Unit tests for symbol handling with Windows compatibility."""

import pytest

from gitstory.cli.symbols import (
    ASCII_SYMBOLS,
    UNICODE_SYMBOLS,
    Symbols,
    _supports_unicode,
    get_symbols,
)


class MockFile:
    """Mock file object with settable encoding attribute."""

    def __init__(self, encoding: str | None = "utf-8"):
        """Initialize mock file with encoding.

        Args:
            encoding: Encoding to report (or None for no encoding)
        """
        self.encoding = encoding


class TestSymbols:
    """Test symbol constants and dataclass."""

    def test_unicode_symbols_defined(self):
        """Test that all Unicode symbols are defined."""
        assert UNICODE_SYMBOLS.SUCCESS == "✓"
        assert UNICODE_SYMBOLS.ERROR == "✗"
        assert UNICODE_SYMBOLS.INFO == "ℹ"
        assert UNICODE_SYMBOLS.WARNING == "⚠"
        assert UNICODE_SYMBOLS.DEBUG == "•"
        assert UNICODE_SYMBOLS.ARROW_RIGHT == "→"
        assert UNICODE_SYMBOLS.BULLET == "•"

    def test_ascii_symbols_defined(self):
        """Test that all ASCII fallback symbols are defined."""
        assert ASCII_SYMBOLS.SUCCESS == "[OK]"
        assert ASCII_SYMBOLS.ERROR == "[X]"
        assert ASCII_SYMBOLS.INFO == "[i]"
        assert ASCII_SYMBOLS.WARNING == "[!]"
        assert ASCII_SYMBOLS.DEBUG == "[*]"
        assert ASCII_SYMBOLS.ARROW_RIGHT == "->"
        assert ASCII_SYMBOLS.BULLET == "*"

    def test_symbols_immutable(self):
        """Test that Symbols is frozen (immutable)."""
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            UNICODE_SYMBOLS.SUCCESS = "X"  # type: ignore


class TestSupportsUnicode:
    """Test Unicode support detection."""

    def test_utf8_encoding_supported(self):
        """Test that UTF-8 encoding is detected as Unicode-capable."""
        mock_file = MockFile(encoding="utf-8")
        assert _supports_unicode(mock_file) is True  # type: ignore

    def test_utf16_encoding_supported(self):
        """Test that UTF-16 encoding is detected as Unicode-capable."""
        mock_file = MockFile(encoding="utf-16")
        assert _supports_unicode(mock_file) is True  # type: ignore

    def test_cp1252_not_supported(self):
        """Test that Windows cp1252 is detected as non-Unicode."""
        mock_file = MockFile(encoding="cp1252")
        assert _supports_unicode(mock_file) is False  # type: ignore

    def test_ascii_not_supported(self):
        """Test that ASCII encoding is detected as non-Unicode."""
        mock_file = MockFile(encoding="ascii")
        assert _supports_unicode(mock_file) is False  # type: ignore

    def test_latin1_not_supported(self):
        """Test that Latin-1 encoding is detected as non-Unicode."""
        mock_file = MockFile(encoding="latin-1")
        assert _supports_unicode(mock_file) is False  # type: ignore

    def test_no_encoding_defaults_to_unicode(self):
        """Test that missing encoding attribute defaults to Unicode support."""

        class MockFileNoEncoding:
            """Mock file without encoding attribute."""

            pass

        mock_file = MockFileNoEncoding()
        assert _supports_unicode(mock_file) is True  # type: ignore

    def test_case_insensitive_encoding_detection(self):
        """Test that encoding detection is case-insensitive."""
        mock_file = MockFile(encoding="UTF-8")  # Uppercase
        assert _supports_unicode(mock_file) is True  # type: ignore

        mock_file = MockFile(encoding="CP1252")  # Uppercase
        assert _supports_unicode(mock_file) is False  # type: ignore


class TestGetSymbols:
    """Test get_symbols() function."""

    def test_returns_unicode_for_utf8(self):
        """Test that UTF-8 stream returns Unicode symbols."""
        mock_file = MockFile(encoding="utf-8")
        symbols = get_symbols(mock_file)  # type: ignore
        assert symbols == UNICODE_SYMBOLS
        assert symbols.SUCCESS == "✓"

    def test_returns_ascii_for_cp1252(self):
        """Test that Windows cp1252 stream returns ASCII symbols."""
        mock_file = MockFile(encoding="cp1252")
        symbols = get_symbols(mock_file)  # type: ignore
        assert symbols == ASCII_SYMBOLS
        assert symbols.SUCCESS == "[OK]"

    def test_force_ascii_flag(self):
        """Test that force_ascii=True always returns ASCII symbols."""
        mock_file = MockFile(encoding="utf-8")  # Even with UTF-8...
        symbols = get_symbols(mock_file, force_ascii=True)  # type: ignore
        assert symbols == ASCII_SYMBOLS  # ...force ASCII
        assert symbols.SUCCESS == "[OK]"

    def test_default_uses_stdout(self):
        """Test that get_symbols() defaults to checking sys.stdout."""
        # This test just ensures it doesn't crash without arguments
        symbols = get_symbols()
        assert isinstance(symbols, Symbols)

    def test_symbols_have_all_attributes(self):
        """Test that returned symbols have all required attributes."""
        symbols = get_symbols()
        assert hasattr(symbols, "SUCCESS")
        assert hasattr(symbols, "ERROR")
        assert hasattr(symbols, "INFO")
        assert hasattr(symbols, "WARNING")
        assert hasattr(symbols, "DEBUG")
        assert hasattr(symbols, "ARROW_RIGHT")
        assert hasattr(symbols, "BULLET")
