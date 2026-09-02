import uuid


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


def short_slug(length: int = 8) -> str:
    return uuid.uuid4().hex[:length]
