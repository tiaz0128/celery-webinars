from celery import Celery
from celery.beat import crontab

app = Celery(
    "worker Celery",
    include=[
        "app.tasks.browser",
    ],
)
app.config_from_object("app.celery_config")

# task 함수 주기 설정
app.conf.beat_schedule = {
    "add-every-seconds": {
        "task": "app.tasks.beat.schedule_today_events",
        "schedule": 30,  # crontab(hour=0, minute=0),  # 자정마다
    },
}


if __name__ == "__main__":
    app.start()
