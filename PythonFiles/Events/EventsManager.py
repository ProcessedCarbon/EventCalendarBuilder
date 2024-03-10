import subprocess
from pathlib import Path
import os
import pytz
import logging
from sys import platform
from tkinter import messagebox
from uuid import uuid4

from Calendar.CalendarInterface import CalendarInterface
from Calendar.CalendarConstants import DEFAULT_CALENDAR
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
import Managers.DirectoryManager as directory_manager
from Managers.DateTimeManager import DateTimeManager
from Managers.TextProcessing import TextProcessingManager
from Events.Event import Event
from GUI.GUIConstants import WARNING_TITLE, NO_CHECKS_MSG, FAILED_TITLE, FAILED_SCHEDULE_MSG, NO_GOOGLE_CONNECTION_MSG, FAILED_ICS_PARSING, NO_OUTLOOK_CONNECTION_MSG

class EventsManager:
    # Directories
    parent_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()
    local_events_dir = Path(os.path.join(parent_dir, 'Local_Events'))
    event_json = 'events.json'
    
    # Temporary event list
    events = []

    # Only contains events that are scheduled by app
    events_db = []

    directory_manager.MakeDirectory(local_events_dir)
    
    def ClearEvents():
        EventsManager.events = []
    
    def UpdateEventsDB():
        '''
        Updates the local event db list by reading from the local events.json
        '''
        # Get event data from JSON
        data = directory_manager.ReadJSON(EventsManager.local_events_dir, EventsManager.event_json)
        if data == None:
            logging.info(f"[{__name__}]NO LOCALLLY SCHEDULED EVENTS")
            return
        
        for d in data:
            event = Event(id=d['id'],
                        name=d['name'],
                        location=d['location'],
                        s_date=d['s_date'],
                        e_date=d['e_date'],
                        start_time=d['start_time'],
                        end_time=d['end_time'],
                        platform=d['platform'],
                        recurring=d['recurring'])
            EventsManager.AddEventToEventDB(event=event, target=EventsManager.events_db, store_object=False)

    # Send only those that are schedule
    def WriteEventDBToJSON():
        '''
        Writes events db to a local events.json file to store locally
        '''
        try:
            db_copy = EventsManager.events_db.copy()

            # convert to json dumpable format
            for e in db_copy:
                    for key in e:
                        if type(e[key]) != str:
                            e[key] = str(e[key])

            # Create JSON file with events
            directory_manager.WriteJSON(EventsManager.local_events_dir, EventsManager.event_json, db_copy)

        except Exception as e:
            logging.error(f'[{__name__}]: {e}')

    def AddEventToEventDB(event:Event, target=None, store_object=True):
        '''
        Takes in an event object and adds it to the target list in this class
        Works with the assumption that event db is updated
        '''
        if target == None:
            logging.warning(f"[{__name__}] MISSING DB TARGET")
            return

        event_dict = event.getEventDict()

        if store_object:
            event_dict['object'] = event

        target.append(event_dict)
        EventsManager.WriteEventDBToJSON()
    
    def RemoveFromEventDB(id:str, target=None)->bool:
        if target == None:
            logging.warning(f"[{__name__}] MISSING DB TARGET")
            return False
        
        logging.info(f'target_id: {id}')
        for e in target:
            if e['id'] == id:
                logging.info(f'found: {e["id"]}')
                target.remove(e)
                EventsManager.WriteEventDBToJSON()
                return True
            
        logging.warning(f"[{__name__}] REMOVE TARGET NOT FOUND!")
        return False

    def UpdateFromEventDB(id:str, update:dict, target=None)->bool:
        if target == None:
            logging.warning(f"[{__name__}] MISSING DB TARGET")
            return False
        
        logging.info(f'target_id: {id}')
        for index, e in enumerate(target):
            if e['id'] == id:
                logging.info(f'found: {e["id"]}')
                target[index] = update
                EventsManager.WriteEventDBToJSON()
                return True
            
        logging.warning(f"[{__name__}] UPDATE TARGET NOT FOUND!")
        return False
    
    def ClearEventsJSON():
        directory_manager.WriteJSON(EventsManager.local_events_dir, EventsManager.event_json, content=None)
    
    def ProcessEvents(events:list[dict]):
        count = 0
        for i in range(len(events)):
            date_time = events[i]["DATE_TIME"].copy()
            if len(date_time) == 0:
                curr_date = DateTimeManager.getCurrentDate()
                formatted_date = curr_date.strftime("%Y-%m-%d")
                date = f"{formatted_date}_{count}"
                events[i]["DATE_TIME"] = {formatted_date : [DateTimeManager.getCurrentTime()]}
                count += 1
            else:
                for d in date_time:
                    time = date_time[d]
                    date = TextProcessingManager.ProcessDate(date_text=str(d))

                    if len(time) > 0: 
                        n_time = TextProcessingManager.ProcessTime(time_text=str(time))
                    else: 
                        n_time = [DateTimeManager.getCurrentTime()]

                    events[i]["DATE_TIME"].pop(d)
                    if isinstance(date, list) and len(date) > 1: 
                        for o in date: 
                            events[i]["DATE_TIME"][f'{o}_{count}'] = n_time
                            count+=1
                    else: 
                        events[i]["DATE_TIME"][f"{date}_{count}"] = n_time
                        count += 1

            # Check how many dates event has, only create and end time if there is only
            # a single date else just treat that date pair as a range and sort them in ascending
            # Also handle the pairing of dates
            for date in events[i]["DATE_TIME"]:
                n = len(events[i]["DATE_TIME"][date])
                if n < 2:
                    # If time only has start time get an end time
                    for j in range(len(events[i]["DATE_TIME"][date])):
                        new_time = [DateTimeManager.AddToTime(events[i]["DATE_TIME"][date][j], hrs=1)] if n > 0 else ["", ""]
                        
                        # Check if end time is greater than start time after adding if its smaller, minus by 1 hr 
                        # and swap the first and new time 
                        if new_time != ["", ""] and DateTimeManager.CompareTimes(str(new_time[0]), str(events[i]["DATE_TIME"][date][j])):
                            new_time = [DateTimeManager.AddToTime(events[i]["DATE_TIME"][date][j], hrs=-1)]
                            tmp = events[i]["DATE_TIME"][date]
                            events[i]["DATE_TIME"][date] = new_time
                            new_time = tmp
                        events[i]["DATE_TIME"][date].extend(new_time)

            events[i]["DATE_TIME"] = dict(sorted(events[i]["DATE_TIME"].items()))
        return events

    def AddEvents(events:list[dict]):
        event_count = 0
        for index, event in enumerate(events):
            keys = list(events[index]['DATE_TIME'].keys())
            
            # If not 2 dates just treat as single event for each
            if len(keys) != 2:
                if len(keys) == 0:
                    return
                
                for k in keys:
                    key_split = k.split('_')
                    start_date = key_split[0]

                    start_time = event['DATE_TIME'][k][0]
                    end_time = event['DATE_TIME'][k][1]

                    n_event = Event(id=uuid4(),
                                    name=event['EVENT'],
                                    location=event["LOC"],
                                    s_date=start_date,
                                    e_date=start_date,
                                    start_time=start_time,
                                    end_time=end_time)
                    EventsManager.AddEventToEventDB(n_event, EventsManager.events)
                    event_count += 1
            else:  
                # If have 2 dates only, by default treat it as a RANGE event
                start_date = keys[0].split('_')[0]
                end_date = keys[1].split('_')[0]

                start_time = event['DATE_TIME'][keys[0]][0]
                end_time = start_time
                recurring = 'None'

                # Check for RECURRING event
                if len(event['DATE_TIME'][keys[0]]) == 2 and len(event['DATE_TIME'][keys[1]]) == 2:
                    if event['DATE_TIME'][keys[0]] == event['DATE_TIME'][keys[1]]:
                        recurring = 'Daily'
                end_time = event['DATE_TIME'][keys[1]][1]
                
                n_event = Event(id=uuid4(),
                                name=event['EVENT'],
                                location=event["LOC"],
                                s_date=start_date,
                                e_date=end_date,
                                start_time=start_time,
                                end_time=end_time,
                                recurring=recurring)
                EventsManager.AddEventToEventDB(n_event, EventsManager.events)
                event_count += 1
    
    # Right now can only handle 1 event only 
    def ScheduleDefault(event, schedule_cb):
        filename = EventsManager.CreateICSFileFromInput(event)
        if filename == None:
            logging.error(f'[{__name__}] FAILED TO CREATE ICS FILE FOR DEFAULT')
            return
        file = CalendarInterface.getICSFilePath(filename)

        # Default run process is Windows
        def schedule_offline():
            os.startfile(file)
            schedule_cb(id=0, platform=DEFAULT_CALENDAR)

        run_process = schedule_offline
        
        # Change to Mac
        if platform == 'darwin':        
            def schedule_mac(): 
                subprocess.run(['open', file])
                schedule_cb(id=0, platform=DEFAULT_CALENDAR)
            run_process = schedule_mac

        res = messagebox.askokcancel(title=WARNING_TITLE, message=NO_CHECKS_MSG)
        if res: 
            run_process()
            
    def ScheduleGoogleCalendar(event, schedule_cb):
        filename = EventsManager.CreateICSFileFromInput(event)
        if filename == None:
            logging.error(f'[{__name__}] FAILED TO CREATE ICS FILE FOR GOOGLE')
            return
        google_event = GoogleCalendarInterface.Parse_ICS(filename)
        
        # Check if can get any event from ICS
        if google_event == None:
            messagebox.showerror(title=FAILED_TITLE, message=FAILED_ICS_PARSING)
            return
        
        # Check for existing events
        existing_events = GoogleCalendarInterface.getEvents(time_min=google_event.getStartDate(), 
                                                            time_max=google_event.getUNTILDate())
        
        # Check if there are is any connection with google
        if existing_events == None:
            messagebox.showerror(title=FAILED_TITLE, message=NO_GOOGLE_CONNECTION_MSG)
            return

        overlapped_events = []
        if len(existing_events) > 0: 
            overlapped_events = GoogleCalendarInterface.EventOverlaps(google_event, existing_events)

        # Method to scheudle google event
        def schedule_google_calendar_event(): 
            id = GoogleCalendarInterface.ScheduleCalendarEvent(googleEvent=google_event)
            if id == '': 
                messagebox.showerror(title=FAILED_TITLE, message=FAILED_SCHEDULE_MSG)
            else: 
                schedule_cb(id=id, platform='Google')

        # Handle clash of events
        if len(overlapped_events) > 0:
            names = [x.getEvent() for x in overlapped_events]
            base_text = ''
            for t in names: 
                base_text += (t + '\n')

            res = messagebox.askokcancel(title=WARNING_TITLE, message=f'Are you sure you want to schedule this event?\nIt clashes with the following events:\n{base_text}')
            if res:
                schedule_google_calendar_event()
        else: 
            schedule_google_calendar_event()

    def ScheduleOutlookCalendar(event, schedule_cb):
        filename = EventsManager.CreateICSFileFromInput(event)
        if filename == None:
            logging.error(f'[{__name__}] FAILED TO CREATE ICS FILE FOR OUTLOOK')
            return ''
        outlook_event = outlook_interface.parse_ics(filename).event

        # Check if can get any event from ICS
        if outlook_event == None:
            messagebox.showerror(title=FAILED_TITLE, message=FAILED_ICS_PARSING)
            return
        
        # Check for any pre-existing event
        cal_events ={}
        try: 
            filter_param = {'$filter': f"start/dateTime ge {outlook_event['start']['dateTime']} and end/dateTime le {outlook_event['end']['dateTime']}"}
            cal_events = outlook_interface.send_flask_req('get_events', param_data=filter_param)[1]['value']
        except: 
            pass

        # Response format
        #(True, {'@odata.context': "", 'value': []})
        if cal_events == {}: 
            messagebox.showerror(title=FAILED_TITLE, message=NO_OUTLOOK_CONNECTION_MSG)
            return

        def schedule_outlook_calendar_event():
            response = outlook_interface.send_flask_req(req='create_event', 
                                                        json_data={'event': outlook_event})
            details = response[1]
            if 'id' not in details: 
                messagebox.showerror(title=FAILED_TITLE, message=FAILED_SCHEDULE_MSG)
            else: 
                schedule_cb(id=details['id'], platform='Outlook')

        # Cannot pass an entire dictionary as a param 
        if len(cal_events) > 0:
            names = [x['subject'] for x in cal_events]
            base_text = ''
            for t in names: 
                base_text += (t + '\n')

            res = messagebox.askokcancel(title=WARNING_TITLE, message=f'Are you sure you want to schedule this event?\nIt clashes with the following events:\n{base_text}')
            if res:
                schedule_outlook_calendar_event()
        else: 
            schedule_outlook_calendar_event()

    # Creates ICS files to be parsed 
    # 1 ICS = should have 1 VEVENT
    # returns names of file created
    def CreateICSFileFromInput(event)->str:
        desp = event["Description"]
        location = event["Location"]
        tz = event['Timezone']
        title = event["Event"]
        ics_s = event["Start_Time_ICS"]
        ics_e = event["End_Time_ICS"]

        ics_s = ics_s.replace(tzinfo=pytz.timezone(tz))
        ics_e = ics_e.replace(tzinfo=pytz.timezone(tz))

        time_difference =  ics_e - ics_s
        hours, remainder = divmod(time_difference.seconds, 3600)

        rrule = {'freq': event["Repeated"].lower(),
                'until': ics_e,
                } if event['Repeated'] != 'None' else {}
        
        # Create ICS File
        file_name = CalendarInterface.CreateICSEvent(e_name=title,
                                                    e_description=desp,
                                                    s_datetime=ics_s,
                                                    e_datetime=ics_e,
                                                    e_location=location,
                                                    rrule=rrule,
                                                    duration=hours)
        return file_name