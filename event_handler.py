# Programmed by Matan Yamin - Final Project.


def create_event_and_insert(service, data):
    """we get here data after inserting to dictionary all parameters
       creating the event to send to the relevant places"""
    event = {  # this event will go the manager and customer calendar in phone
        'summary': "ניקוי עם סקאי קלינר!",
        'location': data["fullAddress"],
        'description': "ניקיון של סקיי קלינר",
        'start': {
            'dateTime': "2021-04-21T09:00:00-07:00",
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': "2021-04-21T17:00:00-07:00",
            'timeZone': 'Asia/Jerusalem',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': data["email"]},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 24 * 60},
            ],
        },
    }
    # connecting to calendar and insert event
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    print("event is done")
    return "event is done"
