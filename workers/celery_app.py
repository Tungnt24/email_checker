from celery import Celery
from multiprocessing import Process
from settings import Config

celery_app = Celery(
    "tasks",
    broker=Config.BROKER_URL,
    include=["workers.tasks"],
    backend=Config.BACKEND_URL,
)

def run():
    w = celery_app.Worker(loglevel="INFO", concurrency=2)
    w.start()


def main():
    w = Process(target=run)
    w.start()


if __name__ == "__main__":
    main()