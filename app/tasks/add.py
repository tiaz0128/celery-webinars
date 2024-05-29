import logging

import random
from time import sleep
from run import app

from celery.exceptions import Reject
import logging


@app.task(queue="scheduler_queue")
def add(x, y):
    sleep(10)
    return x + y


@app.task(queue="task_queue", bind=True, acks_late=True)
def raise_error_add(self, x, y):
    try:
        # 처리 시간 시뮬레이션
        sleep(10)

        logging.info(f"Adding {x} + {y}")

        # 랜덤하게 예외 발생
        if random.choice([True, False]):
            raise Exception("Random failure occurred")

        # 정상 처리
        return x + y

    except Exception as e:
        # 예외 발생 시 Nack를 보내고 다시 큐에 넣음
        logging.error(e)
        raise Reject(e, requeue=True)


@app.task(queue="db_select", bind=True, acks_late=True)
def db_select(self):
    # 처리 시간 시뮬레이션
    sleep(10)

    # 랜덤하게 예외 발생
    return "DB Connect TEST"
