import pytest
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from pytz import timezone

from app.services.google_calendar.api import get_today_webinars
from app.services.google_calendar.token import refresh_token
from app.tasks.browser import run_web_page_task

load_dotenv()


def test_refresh_token():
    refresh_token()


def test_playwright():
    url = "https://www.isc2.org/professional-development/webinars/knowledge-vault?commid=606848?utm_campaign=google-calendar&utm_source=brighttalk-embed&utm_medium=calendar"  # 테스트 페이지
    elapsed_time = 60  # seconds

    tz = timezone("Asia/Seoul")

    now = datetime.now(tz)
    expires_time = (now + timedelta(seconds=3000)).isoformat()
    eta_test_time = (now + timedelta(seconds=20)).isoformat()  # 20초 후 실행

    # celery 실행
    run_web_page_task.apply_async(
        args=[url, elapsed_time],
        eta=eta_test_time,  # eta_time
        expires=expires_time,
    )


def test_get_events():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    webinars = get_today_webinars(user_email)

    tz = timezone("Asia/Seoul")

    for eta_time, url, elapsed_time in webinars:
        now = datetime.now(tz)
        expires_time = (now + timedelta(seconds=elapsed_time)).isoformat()
        eta_test_time = (now + timedelta(seconds=20)).isoformat()

        # celery 실행
        run_web_page_task.apply_async(
            args=[url, elapsed_time],
            eta=eta_test_time,  # eta_time
            expires=expires_time,
        )
