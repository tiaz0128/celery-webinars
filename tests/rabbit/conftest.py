import os
from dotenv import load_dotenv


import pytest
import pika
from pika.adapters.blocking_connection import BlockingChannel

load_dotenv()


@pytest.fixture(scope="session", name="channel")
def setup_channel():
    username = os.getenv("RABBITMQ_DEFAULT_USER")
    password = os.getenv("RABBITMQ_DEFAULT_PASS")
    credentials = pika.PlainCredentials(username, password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost",
            credentials=credentials,
        )
    )
    channel: BlockingChannel = connection.channel()

    yield channel

    connection.close()
