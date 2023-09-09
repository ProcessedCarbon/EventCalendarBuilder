import os.path
import datetime as dt
from dateutil.parser import parse
from Managers.DateTimeManager import DateTimeManager
from Managers.LocationManager import LocationManager
from Managers.ErrorConfig import ErrorCodes
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
    _loc_manager = LocationManager()

    def __init__(self, establish_connection=True):
        self.creds = None

        if establish_connection is True:
            self.ConnectToGoogleCalendar()

    # Tries to establish connection with Google Calendar API
    def ConnectToGoogleCalendar(self):
        print("ESTABLISHING CONNECTION TO GOOGLE CALENDARS......")
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
            print("CONNECTION SUCCESSFUL!")
        except HttpError as error:
            print("CONNECTION FAILFURE")
            print(f'[{str(self.__class__.__name__).upper()}](__init__()): {error}')

    # Calendar event query
    def GetUpcomingCalendarEvent(self, count: int):
        """
        Obtains a list of upcoming count calendar events gotten from google calendar. 
        
        :param count (int): Number of events to get
        return: list of upcoming events from calendar
        """

        if self.service == None:
            ErrorCodes.PrintErrorWithCode(1001)
            return

        now = dt.datetime.now().isoformat() + "Z"

        events_result = self.service.events().list(calendarId='primary', 
                                                timeMin=now,
                                                maxResults=count, 
                                                singleEvents=True,
                                                orderBy='startTime').execute()
            
        events = events_result.get('items', [])

        if not events:
            print("NO UPCOMING EVENTS FOUND")
            return
            
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        return events

    # Event creation
    def CreateCalendarEvent(self, googleEvent: GoogleEvent):
        """
        Creates the google event on the google calendar

        :param googleEvent (GoogleEvent): Google event to be created on calendar
        """
        
        if self.service == None:
            ErrorCodes.PrintErrorWithCode(1001)
            return
        
        if type(googleEvent) is not GoogleEvent:
            ErrorCodes.PrintErrorWithCode(__class__.__name__, "CreateCalendarEvent", 1000)
            print(f"INVALID EVENT OF GIVEN {type(googleEvent)}, LOOKING FOR - {GoogleEvent}")
            return

        
        new_event = self.service.events().insert(calendarId = "primary", body=googleEvent.event).execute()
        print(f"Event created {new_event.get('htmlLink')}")

    # Creates event datatype
    def CreateGoogleEvent(self, event, location, timezone="", time=[], date=[], colorId=1):
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

        date_start = len(date) > 0 and date[0] or None
        time_start = len(time) > 0 and time[0] or None

        date_end = len(date) > 1 and date[1] or None
        time_end = len(time) > 1 and time[1] or None

        curr_date = self._dt_manager.getCurrentDate()
        curr_time = self._dt_manager.getCurrentTime()

        # handle date and time
        start_date_to_use = str(date_start is not None and date_start or curr_date)
        start_time_to_use = str(time_start is not None and time_start or curr_time)

        end_date_to_use = str(date_end is not None and date_end or start_date_to_use)
        end_time_to_use = str(time_end is not None and time_end or self._dt_manager.AddToTime(time=start_time_to_use, hrs=1))
        
        # Handle timezone
        country_gotten = self._loc_manager.getCurrentCountry()
        country =  country_gotten != None and country_gotten or self._loc_manager._default_country
        country_code = self._loc_manager.getCountryCode(country)
        tz = self._dt_manager.getTimeZone(timezone_abrev_=timezone, country_code_=country_code, country_=country)

        return GoogleEvent(event=str(event), 
                           location=str(location), 
                           time_start=start_time_to_use,
                           time_end=end_time_to_use,
                           date_start=start_date_to_use,
                           date_end=end_date_to_use,
                           colorId=colorId,
                           timezone=str(tz)
                           )

# For testing
def main():
    googleCalendar = GoogleCalendarInterface()

    # new_event = googleCalendar.CreateGoogleEvent(event="Test 1", 
    #                                              time_start=None, 
    #                                              time_end=None, 
    #                                              date_start=None, 
    #                                              date_end=None, 
    #                                              location="Test location")
    # print(new_event)
    # googleCalendar.CreateCalendarEvent(googleEvent=new_event)

    # country = str(googleCalendar._loc_manager.getCurrentCountry())
    # country_code = googleCalendar._loc_manager.getCountryCode(country_name=country)
    # tz = googleCalendar._dt_manager.getTimeZone(timezone_abrev_="SGT", country_code_=country_code, country_=country)
    # print("Timezone: " , tz)

if __name__ == "__main__":
    main()


    
