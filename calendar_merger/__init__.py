from .apple.appleEvents import *
from .google.googleEvents import *
from .iCal.createCalendar import createCalendar
from .microsoft.microsoftEvents import *


def get_calendars():
    google_calendar = getGoogleEvents()
    apple_calendar = getAppleEvents()
    microsoft_calendar = getMicrosoftEvents()

    createCalendar(google_calendar, microsoft_calendar, apple_calendar)
    return

