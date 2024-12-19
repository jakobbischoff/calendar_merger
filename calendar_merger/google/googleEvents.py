import datetime
import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import *
from googleapiclient.discovery import *

key_mapping = {
    'name': 'subject',
    'dtstart': 'start',
    'dtend': 'end',
    'webLink': 'webLink',
    'all_day': 'isAllDay',
}


def getGoogleEvents():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')


    transformed_list = []

    for event in events:
        all_day = "dateTime" not in event["start"]
        start_datetime = event["start"].get("dateTime", event["start"].get("date"))
        end_datetime = event["end"].get("dateTime", event["end"].get("date"))

        if not all_day:
            start_datetime = datetime.datetime.fromisoformat(start_datetime)
            start_datetime = start_datetime.replace(tzinfo=None)
            end_datetime = datetime.datetime.fromisoformat(end_datetime)
            end_datetime = end_datetime.replace(tzinfo=None)
        else:
            start_datetime = datetime.date.fromisoformat(start_datetime)
            end_datetime = datetime.date.fromisoformat(end_datetime)

        transformed_event = {
            "name": event["summary"],
            "start": start_datetime,
            "end": end_datetime,
            "link": event["htmlLink"],
            "all_day": all_day
        }
        transformed_list.append(transformed_event)

    return transformed_list