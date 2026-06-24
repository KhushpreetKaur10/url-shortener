from redis_client import redis_client

MAX_REQUESTS = 10
WINDOW_SECONDS = 60


def is_allowed(ip):
    key = f"rate_limit:{ip}"

    try:
        current = redis_client.get(key)

        if current is None:
            redis_client.setex(
                key,
                WINDOW_SECONDS,
                1
            )
            return True

        current = int(current)

        if current >= MAX_REQUESTS:
            return False

        redis_client.incr(key)
        return True

    except Exception:
        # Fail open if Redis is unavailable
        return True