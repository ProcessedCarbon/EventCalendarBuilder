import os.path
import datetime as dt
from dateutil.parser import parse
import DateTimeManager

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
        self._dt_manager = DateTimeManager.Interface()

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
    
    def CreateGoogleDateTimeFormat(self, date, time):
        return str(date) + "T" + str(time)

    def CreateGoogleEvent(self, event, location, time_start=None, time_end=None, date_start=None, date_end=None, colorId=1):
        """
        Returns the google calendar event format with the given entities in placed to be used to parsed to create a new event on google calendars
        https://developers.google.com/calendar/api/v3/reference/events
        
        :param str event: Name of event
        :param str location: Place where the event is to be
        :param str date_start: Start date of event
        :param str date_end: End date of event
        :param str time_start: Start timing of the event
        :param str time_end: End timing of the event
        :return: Event format using google calendars
        """
        curr_date = self._dt_manager.getCurrentDate()
        curr_time = self._dt_manager.getCurrentTime()

        start_date_to_use = date_start is not None and date_start or curr_date
        start_time_to_use = time_start is not None and time_start or curr_time

        end_date_to_use = date_end is not None and date_end or curr_date
        end_time_to_use = time_end is not None and time_end or self._dt_manager.AddToTime(time=curr_time, hrs=1)

        start_DateTime = self.CreateGoogleDateTimeFormat(date=start_date_to_use, time=start_time_to_use)
        end_DateTime = self.CreateGoogleDateTimeFormat(date=end_date_to_use, time=end_time_to_use)
        tz = self._dt_manager.getTimeZone()

        newEvent = {
            "summary" :  'event' in locals() and event or "N/A",
            "location" : 'location' in locals() and location or "N/A",
            "description" : "Test description",
            "colorId" : colorId,
            "start" : {
                "dateTime" : start_DateTime,
                "timeZone" : tz
            },
            "end" : {
                "dateTime" : end_DateTime,
                "timeZone" : tz
            },
            "recurrence" : [
                "RRULE:FREQ=DAILY;COUNT=2"
            ],
            "attendees" : [
                {"email":"nonexistantemail@mail.com"}
            ]
        }

        return newEvent

# For testing
def main():
    googleCalendar = Interface()

    new_event = googleCalendar.CreateGoogleEvent(event="Test 1", time_start=None, time_end=None, date_start=None, date_end=None, location="Test location")
    print(new_event)
    googleCalendar.CreateCalendarEvent(new_event=new_event)

if __name__ == "__main__":
    main()


    
