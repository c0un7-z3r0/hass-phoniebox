"""Utility functions."""


def string_to_bool(value: str) -> bool:
    """Boolean string to boolean converter."""
    if value == "true":
        return True
    return False


def bool_to_string(value: bool) -> str:
    """Boolean string to boolean converter."""
    if value:
        return "true"
    return "false"
