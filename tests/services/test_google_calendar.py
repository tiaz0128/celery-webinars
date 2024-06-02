import pytest
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from pytz import timezone

from app.services.google_calendar.api import get_today_events
from app.services.google_calendar.token import refresh_token
from app.tasks.browser import work_page

load_dotenv()


def test_refresh_token():
    refresh_token()


def test_get_events():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    webinars = get_today_events(user_email)

    tz = timezone("Asia/Seoul")

    for eta_time, url, elapsed_time in webinars:
        now = datetime.now(tz)
        expires_time = (now + timedelta(seconds=elapsed_time)).isoformat()
        eta_test_time = (now + timedelta(seconds=20)).isoformat()

        # celery 실행
        work_page.apply_async(
            args=[url, elapsed_time],
            eta=eta_test_time,  # eta_time
            expires=expires_time,
        )
