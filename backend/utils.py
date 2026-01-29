import os
import secrets
from datetime import datetime, timezone

def generate_id(length: int = 8) -> str:
    return secrets.token_urlsafe(length)[:length]

def get_now(request):
    if os.getenv("TEST_MODE") == "1":
        header = request.headers.get("x-test-now-ms")
        if header:
            return datetime.fromtimestamp(int(header) / 1000, tz=timezone.utc)
    return datetime.now(timezone.utc)
