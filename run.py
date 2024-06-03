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
        "task": "app.tasks.beat.schedule_today_events",
        "schedule": crontab(hour=0, minute=0),  # 자정마다
        # "schedule": 10,  # 30초마다
        "options": {"queue": "schedule-today-events"},  # 특정 큐 지정
    },
}


if __name__ == "__main__":
    app.start()
