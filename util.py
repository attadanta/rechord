from io import StringIO
from hashlib import md5


def sign(params: dict[str, str], secret: str) -> str:
    """
    Compute the request signature (32-character hexadecimal md5 hash) for the given parameters and secret.

    See https://www.last.fm/api/webauth#_6-sign-your-calls
    """
    sorted_keys = sorted([key for key in params.keys() if params[key] is not None])

    message = StringIO()
    message.write("".join(f"{key}{params[key]}" for key in sorted_keys))
    message.write(secret)

    message_string = message.getvalue()
    message_bytes = message_string.encode("utf-8")

    hasher = md5()
    hasher.update(message_bytes)
    return hasher.hexdigest()
