import os

from datetime import datetime, timedelta

from run import app
from app.services.google_calendar.api import get_today_webinars
from app.tasks.browser import run_web_page_task


@app.task
def schedule_today_webinars():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    webinars = get_today_webinars(user_email)

    for eta_time, url, elapsed_time in webinars:
        expires_time = (
            datetime.fromisoformat(eta_time) + timedelta(seconds=elapsed_time)
        ).isoformat()

        # celery 실행
        run_web_page_task.apply_async(
            args=[url, elapsed_time],
            eta=eta_time,
            expires=expires_time,
        )
