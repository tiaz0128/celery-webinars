import pytest
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from pytz import timezone

from app.services.google_dalendar.api import get_today_events
from app.services.google_dalendar.token import refresh_token
from app.tasks.browser import work_page

load_dotenv()


def test_refresh_token():
    refresh_token()


def test_get_events():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    eta_time, url, elapsed_time = get_today_events(user_email)

    tz = timezone("Asia/Seoul")

    now = datetime.now(tz)
    eta_test_time = (now + timedelta(seconds=20)).isoformat()
    expires_time = (now + timedelta(seconds=elapsed_time)).isoformat()

    username = os.getenv("ISC2_USERNAME")
    password = os.getenv("ISC2_PASSWORD")

    if url:
        # celery 실행
        work_page.apply_async(
            args=[url, username, password, elapsed_time],
            eta=eta_test_time,  # eta_time
            expires=expires_time,
        )
