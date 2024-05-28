import os
from celery import Celery

from dotenv import load_dotenv

load_dotenv()


RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")


broker_url = f"pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost//"
result_backend = "rpc://"

# task_serializer = "json"
# result_serializer = "json"
# accept_content = ["json"]
timezone = "UTC"
enable_utc = True
broker_connection_retry_on_startup = True
