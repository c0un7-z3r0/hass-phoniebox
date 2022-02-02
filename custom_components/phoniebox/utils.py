def string_to_bool(value):
    """
    boolean string to boolean converter
    """
    if value == "true":
        return True
    else:
        return False


def bool_to_string(value: bool):
    """
    boolean string to boolean converter
    """
    if value:
        return "true"
    else:
        return "false"
