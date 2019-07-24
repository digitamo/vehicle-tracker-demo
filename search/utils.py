from datetime import datetime


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if isinstance(value, datetime):
        return value.isoformat()
    return None
