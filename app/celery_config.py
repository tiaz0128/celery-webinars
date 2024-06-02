import os

from dotenv import load_dotenv

load_dotenv()


RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")


broker_url = f"pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@localhost//"
result_backend = "rpc://"

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
timezone = "Asia/Seoul"
enable_utc = True
broker_connection_retry_on_startup = True

beat_schedule_filename = "./.temp/celerybeat-schedule"
