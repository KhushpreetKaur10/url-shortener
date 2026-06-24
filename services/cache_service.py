from redis_client import redis_client


def get_cache(key):
    try:
        return redis_client.get(key)
    except:
        return None


def set_cache(key, value, ttl=3600):
    try:
        redis_client.setex(key, ttl, value)
    except:
        pass