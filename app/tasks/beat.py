import os

from datetime import datetime, timedelta

from run import app
from app.services.google_calendar.api import get_today_events
from app.tasks.browser import work_page


@app.task
def schedule_today_events():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    webinars = get_today_events(user_email)

    for eta_time, url, elapsed_time in webinars:
        expires_time = (
            datetime.fromisoformat(eta_time) + timedelta(seconds=elapsed_time)
        ).isoformat()

        # celery 실행
        work_page.apply_async(
            args=[url, elapsed_time],
            eta=eta_time,
            expires=expires_time,
        )
