from environs import Env

env = Env()
env.read_env()

class Config:
    DISPOSABLE_DOMAIN = env.list("DISPOSABLE_DOMAIN")
