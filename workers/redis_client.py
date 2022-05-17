import redis
from settings import RedisConfig


class RedisClient:
    
    def __init__(self) -> None:
        self.redis = redis.Redis(
            host=RedisConfig.REDIS_HOST,
            port=RedisConfig.REDIS_PORT,
            db=RedisConfig.REDIS_DB
        )
    
    def cache_email(self, email: str, second: int) -> None:
        self.redis.set(email, email)
        self.redis.expire(email, second)
    
    def get_email(self, email: str) -> str:
        return self.redis.get(email)
