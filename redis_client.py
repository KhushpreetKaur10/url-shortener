from redis_client import redis_client

def test_redis_connection():
    redis_client.set("test_key", "hello")
    value = redis_client.get("test_key")

    assert value == "hello"
    print("Redis test passed ✔")

if __name__ == "__main__":
    test_redis_connection()
