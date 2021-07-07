from __future__ import print_function
# Programmed by Matan Yamin - Final Project.
import config as cn
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']


def syncalendar_and_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    flagy will tell me what I want to do. write an event or just print
    """
    creds = None
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
    return service


def create_event_and_insert(data):
    service = syncalendar_and_service()
    """we get here data after inserting to dictionary all parameters
       creating the event to send to the relevant places"""
    # this event will go the manager and customer calendar in phone
    event = {
        'summary': "ניקוי עם סקאי קלינר!",
        'location': data["fullAddress"],
        'description': "ניקיון של סקיי קלינר",
        'start': {
            'dateTime': data["date"],
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': data["date"],
            'timeZone': 'Asia/Jerusalem',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': data["email"]},
            {'email': cn.manager_email_contact()},
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
    event = service.events().insert(calendarId='primary', body=event).execute()
    service.events().insert(calendarId='primary', body=event).execute()
    return "OK"