import os
from slowapi import Limiter
from slowapi.util import get_remote_address

_limit = os.environ.get("MAX_REQUESTS_PER_MINUTE", "20")
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{_limit}/minute"])
