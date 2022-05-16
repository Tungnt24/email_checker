from environs import Env

env = Env()
env.read_env()


class Config:
    DISPOSABLE_DOMAIN = env.list("DISPOSABLE_DOMAIN")
    PROXIES = env.list("PROXIES")
    BROKER_URL = env.str("CELERY_BROKER_URL")
    BACKEND_URL = env.str("CELERY_RESULT_BACKEND")
