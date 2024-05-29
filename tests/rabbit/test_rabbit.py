import json
import logging
import random
from uuid import uuid4
import pika
import pytest
from pika.adapters.blocking_connection import BlockingChannel


class TestRabbitMQ:
    @pytest.fixture(autouse=True)
    def setup(self, channel: BlockingChannel):
        self.channel = channel

    def test_rabbit_basic_publish(self):
        self.channel.queue_declare(queue="hello")
        self.channel.basic_publish(
            exchange="",
            routing_key="hello",
            body="Hello World!",
        )

        logging.info(" [x] Sent 'Hello World!'")

    def test_rabbit_basic_consume(self):
        self.channel.queue_declare(queue="hello")
        self.channel.basic_consume(
            queue="hello",
            auto_ack=True,
            on_message_callback=self.callback,
        )

        logging.info(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        logging.info(f" [x] Received {body}")

    def test_rabbit_publish_task(self):
        self.channel.queue_declare(queue="task_queue", durable=True)

        for _ in range(100):
            # Create a message
            message = json.dumps(
                {
                    "id": str(uuid4()),
                    "task": "app.tasks.add.add",
                    "args": [random.randint(1, 100), random.randint(1, 100)],
                }
            )

            # Send the message
            self.channel.basic_publish(
                exchange="",
                routing_key="task_queue",
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_encoding="utf-8",
                    content_type="application/json",
                ),
            )
            print(" [x] Sent 'add task'")

    def test_raise_some_error(self):
        self.channel.queue_declare(queue="task_queue", durable=True)

        for _ in range(100):
            # Create a message
            message = json.dumps(
                {
                    "id": str(uuid4()),
                    "task": "app.tasks.add.raise_error_add",
                    "args": [random.randint(1, 100), random.randint(1, 100)],
                }
            )

            # Send the message
            self.channel.basic_publish(
                exchange="",
                routing_key="task_queue",
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_encoding="utf-8",
                    content_type="application/json",
                ),
            )
            print(" [x] Sent 'add task'")
