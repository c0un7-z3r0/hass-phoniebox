"""Utility functions."""

from typing import Any


def string_to_bool(value: str) -> bool:
    """Boolean string to boolean converter."""
    return value == "true"


def bool_to_string(value: bool) -> str:  # noqa: FBT001
    """Boolean string to boolean converter."""
    if value:
        return "true"
    return "false"


def parse_float_save(val: Any, fallback: float = 0.0) -> float:
    """Try to parse value to float or return fallback."""
    try:
        return float(val)
    except ValueError:
        return fallback


def parse_int_save(val: Any, fallback: int = 0) -> int:
    """Try to parse value to int or return fallback."""
    try:
        return int(val)
    except ValueError:
        return fallback
