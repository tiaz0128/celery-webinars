from celery import Celery
from celery.beat import crontab

app = Celery(
    "worker Celery",
    include=[
        "app.tasks.browser",
        "app.tasks.beat",
    ],
)
app.config_from_object("app.celery_config")

# task 함수 주기 설정
app.conf.beat_schedule = {
    "add-every-seconds": {
        "task": "app.tasks.beat.schedule_today_webinars",
        "schedule": crontab(minute=0),  # 매 시간마다
        # "schedule": 30,  # 30초마다
    },
}


if __name__ == "__main__":
    app.start()
