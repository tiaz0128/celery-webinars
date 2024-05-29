from celery import Celery
from celery.beat import crontab

app = Celery("worker Celery", include=["app.tasks.add", "app.tasks.user"])
app.config_from_object("app.celeryconfig")

# task 함수 주기 설정
app.conf.beat_schedule = {
    "add-every-seconds": {
        "task": "app.tasks.user.schedule_user_add_task",
        "schedule": 5,  # crontab(minute=10),  # 매 10분마다 실행
    },
}


if __name__ == "__main__":
    app.start()
