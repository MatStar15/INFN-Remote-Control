import redis

# Test Redis connection
try:
    r = redis.Redis(host='host.docker.internal', port=6379, db=0)
    print("Connected to Redis!")
    print("Redis is working:", r.ping())
except Exception as e:
    print("Failed to connect to Redis:", e)