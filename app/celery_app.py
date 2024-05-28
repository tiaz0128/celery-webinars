import os
from celery import Celery

from dotenv import load_dotenv

load_dotenv()


RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")

app = Celery(
    "tasks",
    broker=f"pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost//",
    backend="rpc://",
    include=["app.tasks.add"],
)
