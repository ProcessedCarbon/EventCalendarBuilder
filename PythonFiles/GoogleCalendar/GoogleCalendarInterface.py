import os.path
import datetime as dt
from dateutil.parser import parse
from Managers.ErrorConfig import ErrorCodes
from GoogleCalendar.GoogleEvent import GoogleEvent
from Calendar.CalendarInterface import CalendarInterface
from Managers.DateTimeManager import DateTimeManager

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
    creds = None
    service = None
    # Tries to establish connection with Google Calendar API
    def ConnectToGoogleCalendar():
        print("ESTABLISHING CONNECTION TO GOOGLE CALENDARS......")
        if os.path.exists(r'token_path'):
            GoogleCalendarInterface.creds = Credentials.from_authorized_user_file(token_path)
        
        if not GoogleCalendarInterface.creds or not GoogleCalendarInterface.creds.valid:
            if GoogleCalendarInterface.creds and GoogleCalendarInterface.creds.expired and GoogleCalendarInterface.creds.refresh_token:
                GoogleCalendarInterface.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                GoogleCalendarInterface.creds = flow.run_local_server(port = 0)

            with open(token_path, "w") as token:
                token.write(GoogleCalendarInterface.creds.to_json())
        
        try:
            GoogleCalendarInterface.service = build("calendar", 'v3', credentials = GoogleCalendarInterface.creds)
            print("CONNECTION SUCCESSFUL!")
        except HttpError as error:
            print("CONNECTION FAILFURE")
            ErrorCodes.PrintCustomError(error)

    # Calendar event query
    def GetUpcomingCalendarEvent(count: int):
        """
        Obtains a list of upcoming count calendar events gotten from google calendar. 
        
        :param count (int): Number of events to get
        return: list of upcoming events from calendar
        """

        if GoogleCalendarInterface.service == None:
            ErrorCodes.PrintErrorWithCode(1001)
            return

        now = dt.datetime.now().isoformat() + "Z"

        events_result = GoogleCalendarInterface.service.events().list(calendarId='primary', 
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
    def ScheduleCalendarEvent(googleEvent: GoogleEvent)->bool:
        """
        Creates the google event on the google calendar

        :param googleEvent (GoogleEvent): Google event to be created on calendar
        """
        
        if GoogleCalendarInterface.service == None:
            ErrorCodes.PrintErrorWithCode(1001)
            return False
        
        if type(googleEvent) is not GoogleEvent:
            ErrorCodes.PrintErrorWithCode(1000)
            print(f"INVALID EVENT OF GIVEN {type(googleEvent)}, LOOKING FOR - {GoogleEvent}")
            return False

        existing_events = GoogleCalendarInterface.getEvents(time_min=googleEvent.getStartDate(), 
                                                            time_max=googleEvent.getEndDate())

        if GoogleCalendarInterface.EventOverlaps(googleEvent, existing_events):
            return False
                
        new_event = GoogleCalendarInterface.service.events().insert(calendarId = "primary", body=googleEvent.event).execute()
        print(f"Event created {new_event.get('htmlLink')}")
        return True

    # Creates event datatype
    def CreateGoogleEvent(title:str, location:str,  dtstart:str, dtend:str, tzstart:str, tzend:str, colorId=1):
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
        return GoogleEvent(event=title, 
                            location=str(location), 
                            start_datetime=dtstart,
                            end_datetime=dtend,
                            colorId=colorId,
                            tzstart=tzstart,
                            tzend=tzend
                           )

    def Parse_ICS(ics:str):
        if GoogleCalendarInterface.service == None:
            ErrorCodes.PrintErrorWithCode(1001)
            return
        
        events = []
        ics_file = CalendarInterface.ReadICSFile(ics)
        for component in ics_file.walk():
              if component.name == "VEVENT":
                    start_datetime = component.get('dtstart').dt.isoformat()
                    end_datetime = component.get('dtend').dt.isoformat()
                    tzstart = str(component.get('dtstart').dt.tzinfo)
                    tzend = str(component.get('dtstart').dt.tzinfo)

                    events.append(GoogleCalendarInterface.CreateGoogleEvent(title=component.get('name'),
                                                                            location=component.get("location"),
                                                                            dtstart=start_datetime,
                                                                            dtend=end_datetime,
                                                                            tzstart=tzstart,
                                                                            tzend=tzend
                                                                        ))
        return events
    
    def getEvents(calendar_id='primary', time_min=None, time_max=None)->list[GoogleEvent]:
        """Get events from a specific calendar within a time range."""
        existing = GoogleCalendarInterface.service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute().get('items', [])
        existing_google_events = [GoogleCalendarInterface.CreateGoogleEvent(
                                                                            title=x['summary'],
                                                                            location=x['location'] if "location" in x else "", # Done this way as might be empty
                                                                            dtstart=x['start']['dateTime'],
                                                                            tzstart=x['start']['timeZone'],
                                                                            dtend=x['end']['dateTime'],
                                                                            tzend=x['end']['timeZone']
                                                                        ) for x in existing]
        return existing_google_events  

    def EventOverlaps(new_event:GoogleEvent, existing_events:list[GoogleEvent])->bool:
        """Check if the new event overlaps with any existing events."""
        new_event_start = new_event.getStartDate().replace("T", " ")
        new_event_end = new_event.getEndDate().replace("T", " ")

        for event in existing_events:
            event_start = event.getStartDate().replace("T", " ")
            event_end = event.getEndDate().replace("T", " ")

            if DateTimeManager.hasDateTimeClash(new_event_start, new_event_end, event_start, event_end):
                print(f'Event to schedule {new_event.getEvent().upper()} has clash with {event.getEvent().upper()}!')
                return True
        return False
