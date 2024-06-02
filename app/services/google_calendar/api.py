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


def get_today_events(user_email):
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
            if location == "BrightTALK":
                # and start.startswith(datetime.now().strftime("%Y-%m-%d")):

                # 정규 표현식을 사용하여 첫 번째 https부터 \n\n 이전까지 추출
                pattern = r"https[^\n]+"
                match = re.search(pattern, event["description"])
                if match:
                    url = match.group()
                    logging.info(start)
                    logging.info(event["summary"])
                    logging.info(url)

                    elapsed_time = datetime.fromisoformat(end) - datetime.fromisoformat(
                        start
                    )

                    webinars.append((start, url, elapsed_time.total_seconds()))

        return webinars

    except HttpError as error:
        logging.error(f"An error occurred: {error}")
        return []
