from environs import Env

env = Env()
env.read_env()


class DomainConfig:
    DISPOSABLE_DOMAIN = env.list("DISPOSABLE_DOMAIN")


class ProxyConfig:
    PROXIES = env.list("PROXIES")


class CeleryConfig:
    BROKER_URL = env.str("CELERY_BROKER_URL")
    BACKEND_URL = env.str("CELERY_RESULT_BACKEND")


class RedisConfig:
    REDIS_HOST = env.str("REDIS_HOST")
    REDIS_PORT = env.int("REDIS_PORT")
    REDIS_DB = env.int("REDIS_DB")
