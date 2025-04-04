import redis

def connect_with_redis_server():
    connection = redis.Redis(
        host = 'localhost',
        port = 6379,
        decode_responses=True
    )
    if connection.ping():
        print(":) successfully connected with redis server.")
        return connection
    else:
        print(":( failed to connected with redis server.")
        return None

def redis_push(key, value, redis_server):
    redis_server.set(str(key), str(value))

def redis_get(key, redis_server):
    value = redis_server.get(key)
    return value

def disconnect_from_redis_server(redis_server):
    if redis_server:
        redis_server.close()
        print(":( Disconnected from Redis server.")

if __name__ == "__main__":
    redis_server = connect_with_redis_server()
    print(redis_get("51_452465", redis_server))