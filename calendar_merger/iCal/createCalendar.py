from dotenv import load_dotenv
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, date
load_dotenv()


def createCalendar(google_events, microsoft_events, apple_events):
    cal = Calendar()
    cal.add("prodid", "Calender created by Calendar Merger")
    cal.add("version", "2.0")
    cal.add("method", "PUBLISH")
    cal.add("created", datetime.now())
    cal.add('charset', 'UTF-8')
    counter = 0

    for x, event in enumerate(apple_events):

        name = event.get('name', 'Unnamed Event')
        description = event.get('description', None)
        start = event.get('start', None)
        end = event.get('end', None)
        organizer = event.get('organizer', None)
        location = event.get('location', None)
        attachment = event.get('attachment', None)
        url = event.get('url', None)

        event = Event()
        event.add('SUMMARY', name)
        event.add('DESCRIPTION', description)
        event.add('DTSTART', start)
        event.add('DTEND', end)
        event.add('DTSTAMP', datetime.now())
        event.add('ATTACHMENT', attachment)
        event.add('URL', url)
        event.add('UID', f"{x}")
        event.add('PRIORITY', 1)
        event.add('LOCATION', location)
        if organizer:
            event.add('ORGANIZER', f"CN={organizer}")
        cal.add_component(event)
        counter += 1

    for event in google_events:
        name = event.get('name', 'Unnamed Event')
        description = event.get('link', None)
        start = event.get('start', None)
        end = event.get('end', None)
        url = event.get('link', None)

        event = Event()
        event.add('SUMMARY', name)
        event.add('DESCRIPTION', description)
        event.add('DTSTART', start)
        event.add('DTEND', end)
        event.add('DTSTAMP', datetime.now())
        event.add("URL", url)
        event.add('UID', f"{counter}")
        event.add('PRIORITY', 1)
        cal.add_component(event)
        counter += 1

    for event in microsoft_events:
        name = event.get('name', 'Unnamed Event')
        description = event.get('link', None)
        start = event.get('start', None)
        end = event.get('end', None)
        url = event.get('link', None)

        event = Event()
        event.add('SUMMARY', name)
        event.add('DESCRIPTION', description)
        event.add('DTSTART', start)
        event.add('DTEND', end)
        event.add('DTSTAMP', datetime.now())
        event.add("URL", url)
        event.add('UID', f"{counter}")
        event.add('PRIORITY', 1)
        cal.add_component(event)
        counter += 1

    calendar_filename = "my_calendar.ics"
    with open(calendar_filename, 'wb') as f:
        f.write(cal.to_ical())

    with open(calendar_filename, 'r') as f:
        calendar_content = f.read()

    print(calendar_content)