import os
from dotenv import load_dotenv

from datetime import datetime, timedelta

from app.services.google_dalendar.api import get_today_events
from app.tasks.browser import work_page

load_dotenv()


def schedule_today_events():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    webinars = get_today_events(user_email)

    id = os.getenv("ISC2_USERNAME")
    pw = os.getenv("ISC2_PASSWORD")

    for eta_time, url, elapsed_time in webinars:
        expires_time = (
            datetime.fromisoformat(eta_time) + timedelta(seconds=elapsed_time)
        ).isoformat()

        # celery 실행
        work_page.apply_async(
            args=[url, id, pw, elapsed_time],
            eta=eta_time,
            expires=expires_time,
        )
