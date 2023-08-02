import os.path
import datetime as dt
from dateutil.parser import parse
from Managers.DateTimeManager import DateTimeManager
from GoogleCalendar.GoogleEvent import GoogleEvent

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
GoogleCalendarAPI_path = "./GoogleCalendarAPI/"
token_path = GoogleCalendarAPI_path + "token.json"
credentials_path = GoogleCalendarAPI_path + "credentials.json"

class GoogleCalendarInterface:
    _dt_manager = DateTimeManager()
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
    def GetLatestCalendarEvent(self, count: int):
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
    def CreateCalendarEvent(self, googleEvent: GoogleEvent):
        if self.service == None:
            print("Missing service!")
            return
        
        new_event = self.service.events().insert(calendarId = "primary", body=googleEvent.event).execute()
        print(f"Event created {new_event.get('htmlLink')}")

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

        start_date_to_use = str(date_start is not None and date_start or curr_date)
        start_time_to_use = str(time_start is not None and time_start or curr_time)

        end_date_to_use = str(date_end is not None and date_end or start_date_to_use)
        end_time_to_use = str(time_end is not None and time_end or self._dt_manager.AddToTime(time=start_time_to_use, hrs=1))
        
        tz = str(self._dt_manager.getTimeZone())

        return GoogleEvent(event=str(event), 
                           location=str(location), 
                           time_start=start_time_to_use,
                           time_end=end_time_to_use,
                           date_start=start_date_to_use,
                           date_end=end_date_to_use,
                           colorId=colorId,
                           timezone=tz
                           )

# For testing
def main():
    googleCalendar = GoogleCalendarInterface()

    new_event = googleCalendar.CreateGoogleEvent(event="Test 1", 
                                                 time_start=None, 
                                                 time_end=None, 
                                                 date_start=None, 
                                                 date_end=None, 
                                                 location="Test location")
    print(new_event)
    googleCalendar.CreateCalendarEvent(googleEvent=new_event)

if __name__ == "__main__":
    main()


    
