from app.core.config import settings
import hashlib
from datetime import datetime


class RateLimiter:
    def __init__(self):
        # In-memory storage for rate limiting (no redis needed)
        self.storage = {}
        self.free_daily_limit = settings.FREE_DAILY_LIMIT

    def _get_key(self, client_ip: str) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        ip_hash = hashlib.md5(client_ip.encode()).hexdigest()
        return f"{today}:{ip_hash}"

    def check_and_increment(self, client_ip: str) -> tuple[bool, int]:
        """Check if allowed, increment if allowed, return (allowed, remaining)"""
        key = self._get_key(client_ip)

        # Get current count
        current = self.storage.get(key, 0)

        if current >= self.free_daily_limit:
            return False, 0
        else:
            self.storage[key] = current + 1
            return True, self.free_daily_limit - (current + 1)

    def get_remaining(self, client_ip: str) -> int:
        """Get remaining free attempts"""
        key = self._get_key(client_ip)
        current = self.storage.get(key, 0)
        return max(0, self.free_daily_limit - current)


rate_limiter = RateLimiter()
