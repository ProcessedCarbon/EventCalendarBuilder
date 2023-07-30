import os.path
import datetime as dt
from dateutil.parser import parse
import wordninja

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
GoogleCalendarAPI_path = "./GoogleCalendarAPI/"
token_path = GoogleCalendarAPI_path + "token.json"
credentials_path = GoogleCalendarAPI_path + "credentials.json"

class Interface:
    def __init__(self):
        self.creds = None

        if os.path.exists(r'token_path'):
            self.creds = Credentials.from_authorized_user_file(token_path)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                self.creds = flow.run_local_server(port = 0)

            with open(token_path, "w") as token:
                token.write(self.creds.to_json())
        
        try:
            self.service = build("calendar", 'v3', credentials = self.creds)
        except HttpError as error:
            print("Err occured: ", error)

    # Calendar event query
    def GetLatestCalendarEvent(self, count):
        if self.service == None:
            print("Missing service!")
            return

        now = dt.datetime.now().isoformat() + "Z"

        events_result = self.service.events().list(calendarId='primary', 
                                                timeMin=now,
                                                maxResults=count, 
                                                singleEvents=True,
                                                orderBy='startTime').execute()
            
        events = events_result.get('items', [])

        if not events:
            print("Zero upcoming events found!")
            return
            
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    # Event creation
    def CreateCalendarEvent(self, new_event):
        if self.service == None:
            print("Missing service!")
            return

        new_event = self.service.events().insert(calendarId = "primary", body=new_event).execute()
        print(f"Event created {new_event.get('htmlLink')}")
    
    def CreateEvent(event, time, date, location):
        """
        Returns the google calendar event format with the given entities in placed to be used to parsed to create a new event on google calendars

        :param str event: Name of event
        :param str location: Place where the event is to be
        :param str date: Start and end Dates of the event
        :param str time: Start and end times of the event
        :return: Event format using google calendars
        """

        parsed_date = parse(date)
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        print("Formatted Date: ", formatted_date)

        splitted_time = wordninja.split(time)
        

        newEvent = {
            "summary" :  'event' in locals() and event or "N/A",
            "location" : 'location' in locals() and location or "N/A",
            "description" : "Test description",
            "colorId" : 6,
            "start" : {
                "dateTime" : "2023-07-04T22:00:00",
                "timeZone" : "Singapore"
            },
            "end" : {
                "dateTime" : "2023-07-04T23:00:00",
                "timeZone" : "Singapore"
            },
            "recurrence" : [
                "RRULE:FREQ=DAILY;COUNT=2"
            ],
            "attendees" : [
                {"email":"nonexistantemail@mail.com"}
            ]
        }

        return newEvent


    
