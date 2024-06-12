import re
import logging

from datetime import datetime
from pytz import timezone


from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = ".temp/service-account-file.json"

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials(scopes):
    return Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)


def get_today_webinars(user_email):
    creds = get_credentials(SCOPES)
    webinars = []

    try:
        service = build("calendar", "v3", credentials=creds)

        tz = timezone("Asia/Seoul")

        # Call the Calendar API
        now = datetime.now(tz).isoformat()
        logging.info("Getting the upcoming 10 events")

        events_result = (
            service.events()
            .list(
                calendarId=user_email,
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            logging.info("No upcoming events found.")
            return []

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            location = event.get("location")

            # 오늘 00:00:00 부터 시작하는 BrightTALK 이벤트만 추출
            if is_webinar(start, location):
                url = get_webinar_url(event)

                elapsed_time = datetime.fromisoformat(end) - datetime.fromisoformat(
                    start
                )

                logging.info(f"[webinar {len(webinars) + 1}]")
                logging.info(f"\t\t{start}")
                logging.info(f"\t\t{event["summary"]}")
                logging.info(f"\t\t{url}")

                webinars.append((start, url, elapsed_time.total_seconds()))

        return webinars

    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return []


def get_webinar_url(event):
    # 첫 번째 https부터 \n\n 이전까지 추출
    pattern = r"https[^\n]+"
    match = re.search(pattern, event["description"])

    return match.group()


def is_webinar(start, location):
    tz = timezone("Asia/Seoul")

    return location == "BrightTALK" and start.startswith(
        datetime.now(tz).strftime("%Y-%m-%d %H")
    )
