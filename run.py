import random
from celery import Celery

app = Celery("worker Celery", include=["app.tasks.add"])
app.config_from_object("app.celeryconfig")

# task 함수 주기 설정
app.conf.beat_schedule = {
    "add-every-seconds": {
        "task": "app.tasks.add.db_select",
        "schedule": 10.0,  #  crontab(hour=0, minute=0),  # 매일 자정에 실행
    },
}


if __name__ == "__main__":
    app.start()
