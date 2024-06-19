"""Tests for the utils."""

from custom_components.phoniebox.utils import (
    bool_to_string,
    parse_float_save,
    parse_int_save,
    string_to_bool,
)


def test_parse_float_save() -> None:
    """Test parsing of float."""
    val = parse_float_save("10")
    assert val == 10.0
    assert isinstance(val, float)
    val = parse_float_save(val="-10", fallback=2.3)
    assert val == -10.0
    assert isinstance(val, float)
    val = parse_float_save(val="1a0")
    assert val == 0
    assert isinstance(val, float)


def test_parse_float_save_fallback() -> None:
    """Test parsing of float failing."""
    val = parse_float_save("-1a0")
    assert val == 0.0
    assert isinstance(val, float)
    val = parse_float_save(val="-10a", fallback=2.3)
    assert val == 2.3
    assert isinstance(val, float)
    val = parse_float_save(val="-10a", fallback=-1.2)
    assert val == -1.2
    assert isinstance(val, float)


def test_parse_int_save() -> None:
    """Test parsing of int."""
    val = parse_int_save("10")
    assert val == 10
    assert isinstance(val, int)

    val = parse_int_save(val="-10", fallback=2)
    assert val == -10
    assert isinstance(val, int)

    val = parse_int_save(val="1a0")
    assert val == 0
    assert isinstance(val, int)


def test_parse_int_save_fallback() -> None:
    """Test parsing of int failing."""
    val = parse_int_save("-1a0")
    assert val == 0.0
    assert isinstance(val, int)
    val = parse_int_save(val="-10a", fallback=2)
    assert val == 2
    assert isinstance(val, int)
    val = parse_int_save(val="-10a", fallback=-1)
    assert val == -1
    assert isinstance(val, int)


def test_bool_to_string() -> None:
    """Test the util function to stringify bool."""
    val = bool_to_string(True)
    assert isinstance(val, str)
    assert val == "true"

    val = bool_to_string(False)
    assert isinstance(val, str)
    assert val == "false"


def test_string_to_bool() -> None:
    """Test the util function to parse string to boolean."""
    val = string_to_bool("true")
    assert isinstance(val, bool)
    assert val is True

    val = string_to_bool("false")
    assert isinstance(val, bool)
    assert val is False

    val = string_to_bool("any thing else")
    assert isinstance(val, bool)
    assert val is False
