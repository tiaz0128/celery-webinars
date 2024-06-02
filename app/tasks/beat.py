import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from pytz import timezone

from app.services.google_dalendar.api import get_today_events
from app.tasks.browser import work_page

load_dotenv()


def schedule_today_events():
    user_email = os.getenv("GOOGLE_CALENDAR_USER_EMAIL")
    eta_time, url, elapsed_time = get_today_events(user_email)

    # eta_test_time = (now + timedelta(seconds=20)).isoformat()

    tz = timezone("Asia/Seoul")

    now = datetime.now(tz)
    expires_time = (now + timedelta(seconds=elapsed_time)).isoformat()

    id = os.getenv("ISC2_USERNAME")
    pw = os.getenv("ISC2_PASSWORD")

    if url:
        # celery 실행
        work_page.apply_async(
            args=[url, id, pw, elapsed_time],
            eta=eta_time,
            expires=expires_time,
        )
