import requests
import json
import datetime
import dateutil.parser

from django.conf import settings

API_URL = "https://www.googleapis.com/calendar/v3/calendars/{}/events?timeMin={}&timeMax={}&singleEvents=True&key={}"
API_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def get_calendar_events(dt):
  """
  Return a list of events that are occuring at datetime
  dt on the calendar specified in the settings.
  """

  time_min = dt
  time_max = time_min + datetime.timedelta(days=1)

  time_min_s = time_min.strftime(API_DATETIME_FORMAT)
  time_max_s = time_max.strftime(API_DATETIME_FORMAT)

  url = API_URL.format(settings.GOOGLE_CALENDAR_ID, time_min_s, time_max_s, settings.GOOGLE_API_KEY)

  response = requests.get(url).json()
  items = response['items']

  events = []

  for item in items:
    name = item.get('summary', '')
    location = item.get('location', '')
   
    start_pair = item.get('start', {})
    start = start_pair.get('dateTime', start_pair.get('date', None))
    start = dateutil.parser.parse(start)

    end_pair = item.get('end', {})
    end = end_pair.get('dateTime', end_pair.get('date', None))
    end = dateutil.parser.parse(end)

    if not start.tzinfo:
      start = start.replace(tzinfo=dt.tzinfo)

    if not end.tzinfo:
      end = end.replace(tzinfo=dt.tzinfo)

    if start <= dt < end:
      event = {
        'name': name,
        'location': location,
        'start': start,
        'end': end
      }

      events.append(event)

  return events
