import datetime
import os
from pyicloud import PyiCloudService
import sys
from dotenv import load_dotenv
load_dotenv()


key_mapping = {
    'name': 'title',
    'description': 'description',
    'start': 'startDate',
    'end': 'endDate',
    'all_day': 'allDay',
    'attachment': 'attachments',
    'location': 'location',
    'url' : 'url'
}

def getAppleEvents():
    api = PyiCloudService(os.environ['APPLE_EMAIL'], os.environ['APPLE_PASSWORD'])
    if not api.is_trusted_session:
        if api.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = api.validate_2fa_code(code)
            print("Code validation result: %s" % result)
        else:
            sys.exit()


    from_dt = datetime.datetime.now().date()
    to_dt = from_dt.replace(year=from_dt.year + 2)
    from_dt = from_dt.strftime("%Y-%m-%d")
    to_dt = to_dt.strftime("%Y-%m-%d")

    calendar = api.calendar.events(from_dt, to_dt)
    specific_pguid = os.environ['PGUID']

    filtered_calendar = [event for event in calendar if event.get("pGuid") == specific_pguid]

    transformed_list = [
        {key: event.get(value, None) for key, value in key_mapping.items()}
        for event in filtered_calendar
    ]
    for event in transformed_list:
        if event['all_day']:
            start_date = event['start']
            start_year, start_month, start_day = start_date[1:4]
            dt_start = datetime.date(start_year, start_month, start_day)
            end_date = event['end']
            end_year, end_month, end_day = end_date[1:4]
            dt_end = datetime.date(end_year, end_month, end_day)
        else:
            start_date = event['start']
            start_year, start_month, start_day, start_hour, start_minute, start_second = start_date[1:7]
            dt_start = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second // 1000)  # Convert milliseconds to seconds
            end_date = event['end']
            end_year, end_month, end_day, end_hour, end_minute, end_second = end_date[1:7]
            dt_end = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second // 1000)
        event['start'] = dt_start
        event['end'] = dt_end

    return transformed_list
