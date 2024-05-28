import logging
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
