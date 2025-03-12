from celery import Celery
import redis

import logging

celery = Celery('test_app', broker = "redis://host.docker.internal:6379/0", backend = "redis://host.docker.internal:6379/0")

def test_celery_connection():
    """Test connection to Celery broker (Redis)"""
    try:
        # Create Redis client
        redis_client = redis.from_url("redis://host.docker.internal:6379/0")

        # Test Redis connection with ping
        redis_client.ping()
        print("Successfully connected to Redis broker")

        # Test Celery app connection

        # Try to connect to broker


        celery.log.setup()
        logging.getLogger('celery').setLevel(logging.DEBUG)


        # Clean up connections
        conn.release()
        redis_client.close()
        return True

    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        return False
    except Exception as e:
        print(f"Failed to connect to Celery broker: {e}")
        return False


if __name__ == '__main__':

    test_celery_connection()