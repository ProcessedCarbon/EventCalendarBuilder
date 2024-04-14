import os.path
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import re

from Calendar.GoogleCalendar.GoogleEvent import GoogleEvent
from Calendar.CalendarInterface import CalendarInterface
from Managers.DateTimeManager import DateTimeManager
import Managers.DirectoryManager as directory_manager
from GUI.GUIConstants import FAILED_TITLE, NO_GOOGLE_CONNECTION_MSG

SCOPES = ['https://www.googleapis.com/auth/calendar']

MAIN_PATH = directory_manager.getCurrentFileDirectory(__file__)
MISC_PATH = directory_manager.getFilePath(MAIN_PATH, 'GoogleCalendarAPI')
TOKEN_PATH = directory_manager.getFilePath(MISC_PATH, 'token.json')
CREDS_PATH = directory_manager.getFilePath(MISC_PATH, 'credentials.json')

class GoogleCalendarInterface:
    creds = None
    service = None
    # Tries to establish connection with Google Calendar API
    def ConnectToGoogleCalendar():
        logging.info("ESTABLISHING CONNECTION TO GOOGLE CALENDARS......")
        if os.path.exists(r'token_path'):
            GoogleCalendarInterface.creds = Credentials.from_authorized_user_file(TOKEN_PATH)
        
        if not GoogleCalendarInterface.creds or not GoogleCalendarInterface.creds.valid:
            if GoogleCalendarInterface.creds and GoogleCalendarInterface.creds.expired and GoogleCalendarInterface.creds.refresh_token:
                GoogleCalendarInterface.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
                GoogleCalendarInterface.creds = flow.run_local_server(port = 0)

            with open(TOKEN_PATH, "w") as token:
                token.write(GoogleCalendarInterface.creds.to_json())
        
        try:
            GoogleCalendarInterface.service = build("calendar", 'v3', credentials = GoogleCalendarInterface.creds)
            logging.info(f"[{__name__}] CONNECTION SUCCESSFUL")
            return True
        except HttpError as error:
            logging.error(f"[{__name__}] CONNECTION FAILURE WITH {error}")
            return False

    # Calendar event query
    def GetUpcomingCalendarEvent(count: int):
        """
        Obtains a list of upcoming count calendar events gotten from google calendar. 
        
        :param count (int): Number of events to get
        return: list of upcoming events from calendar
        """

        if GoogleCalendarInterface.service == None:
            logging.warning(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return

        now = dt.datetime.now().isoformat() + "Z"

        events_result = GoogleCalendarInterface.service.events().list(calendarId='primary', 
                                                                        timeMin=now,
                                                                        maxResults=count, 
                                                                        singleEvents=True,
                                                                        orderBy='startTime').execute()
            
        events = events_result.get('items', [])

        if not events:
            logging.info("NO UPCOMING EVENTS FOUND")
            return

        return events

    # Event creation
    def ScheduleCalendarEvent(googleEvent: GoogleEvent)->str:
        """
        Creates the google event on the google calendar

        :param googleEvent (GoogleEvent): Google event to be created on calendar
        """
        
        if GoogleCalendarInterface.service == None:
            logging.error(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return '', []
        
        if type(googleEvent) is not GoogleEvent:
            logging.error(f"[{__name__}] INVALID EVENT OF GIVEN {type(googleEvent)}, LOOKING FOR - {GoogleEvent}")
            return '', []
    
        new_event = GoogleCalendarInterface.service.events().insert(calendarId = "primary", body=googleEvent.event).execute()
        logging.info(f"New event {new_event} created at {new_event.get('htmlLink')}")
        return new_event['id']

    # Creates event datatype
    def CreateGoogleEvent(title:str, location:str,  dtstart:str, dtend:str, tzstart:str, tzend:str, rrule:str, description=''):
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
                            tzstart=tzstart,
                            tzend=tzend,
                            rrule=rrule,
                            description=description)

    # Only expecting 1 event per ics
    def Parse_ICS(ics:str)->GoogleEvent:        
        ics_file = CalendarInterface.ReadICSFile(ics)
        vEvent = False
        alert = None

        for component in ics_file.walk():
            if component.name == "VEVENT":
                start_datetime = component.get('dtstart').dt.isoformat()
                end_datetime = component.get('dtend').dt.isoformat()
                tzstart = str(component.get('dtstart').dt.tzinfo)
                tzend = str(component.get('dtstart').dt.tzinfo)
                name = component.get('name')
                location = component.get("location")
                desc = component.get('description')
                rule='RRULE:' + component.get('rrule').to_ical().decode(errors="ignore")+'Z' if component.get('rrule') is not None else ''
                vEvent = True

            if component.name == "VALARM":
                # Use regular expressions to extract the trigger time
                match = re.search(r'(\d{2}:\d{2}:\d{2})', str(component.get('trigger')))
                if match:
                    trigger_time = match.group(0)[3:5]
                    diff = 60 - int(trigger_time)
                    alert = diff if (diff != 0) else 60

        return GoogleEvent(event=name,
                            location=location,
                            start_datetime=start_datetime,
                            end_datetime=end_datetime,
                            tzstart=tzstart,
                            tzend=tzend,
                            rrule=str(rule) if rule != '' else [],
                            description=desc,
                            alert=alert if alert != None else 10) if vEvent else None
    
    def getEvents(calendar_id='primary', time_min=None, time_max=None)->list[GoogleEvent]:
        if GoogleCalendarInterface.service == None:
            logging.warning(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return None
        
        """Get events from a specific calendar within a time range."""
        existing = GoogleCalendarInterface.service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max).execute().get('items', [])
        existing_google_events = [GoogleEvent(event=x['summary'],
                                            location=x['location'] if "location" in x else "", # Done this way as might be empty
                                            start_datetime=x['start']['dateTime'],
                                            tzstart=x['start']['timeZone'],
                                            end_datetime=x['end']['dateTime'],
                                            tzend=x['end']['timeZone'],
                                            rrule=x['recurrence'] if 'recurrence' in x else '',
                                            description=x['description'] if 'description' in x else ''
                                            ) for x in existing]
        
        return existing_google_events  

    def EventOverlaps(new_event:GoogleEvent, existing_events:list[GoogleEvent])->bool:
        """Check if the new event overlaps with any existing events."""
        overlapped_events = []
        # 2023-01-31 18:00:00+08:00
        new_event_start = new_event.getStartDate().replace("T", " ") 
        new_event_end = new_event.getUNTILDate().replace("T", " ")

        for event in existing_events:
            event_start = event.getStartDate().replace("T", " ")
            event_end = event.getEndDate().replace("T", " ")

            if DateTimeManager.hasDateTimeClash(new_event_start, new_event_end, event_start, event_end):
                overlapped_events.append(event)
        return overlapped_events #False
    
    def DeleteEvent(id:str):
        if GoogleCalendarInterface.service == None:
            logging.warning(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return False,''
        
        try:
            GoogleCalendarInterface.service.events().delete(calendarId='primary', eventId=id).execute()
            logging.info(f"[{__name__}] EVENT DELETED SUCCESSFULLY")
            return True,''
        except HttpError as e:
            error_details = e.error_details[0]
            if 'reason' in error_details['reason'] and error_details['reason'] != '':
                return False, error_details['reason']
            else: return False, 'Unknown Reason, Proceeding to Deletion'
    
    def UpdateEvent(id:str, update: dict):
        print('Update: ', update)
        if GoogleCalendarInterface.service == None:
            logging.warning(f"[{__name__}] MISSING CONNECTION TO GOOGLE CALENDARS, PLEASE CONNECT TO GOOGLE CALENDARS FIRST")
            return False,''
        
        try:
            GoogleCalendarInterface.service.events().update(calendarId='primary', eventId=id, body=update).execute()
            logging.info(f"[{__name__}] EVENT UPDATED SUCCESSFULLY")
            return True,''
        except HttpError as e:
            error_details = e.error_details[0]
            if 'reason' in error_details['reason'] and error_details['reason'] != '':
                return False, error_details['reason']
            else: return False, 'Unknown Reason, Update cancelled'