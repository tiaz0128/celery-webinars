import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def refresh_token(scopes):
    creds = None

    if os.path.exists(".temp/token.json"):
        creds = Credentials.from_authorized_user_file(".temp/token.json", scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                ".temp/credentials.json", scopes
            )
            creds = flow.run_local_server(port=0)

        with open(".temp/token.json", "w") as token:
            token.write(creds.to_json())

    return creds
