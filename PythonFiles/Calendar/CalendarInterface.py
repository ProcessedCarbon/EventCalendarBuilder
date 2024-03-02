import icalendar
from icalendar import Calendar, Event, vCalAddress, vText
from pathlib import Path
from datetime import timedelta
from uuid import uuid4
import logging

import Managers.DirectoryManager as directory_manager
from Managers.TextProcessing import TextProcessingManager

class CalendarInterface:
    _cal = Calendar()
    _cal.add('prodid', '-//My calendar product//example.com//')
    _cal.add('version', '2.0')

    _default_ics_file = 'to_schedule'

    # Directories
    parent_dir = directory_manager.getCurrentFileDirectory(__file__)
    _main_dir = directory_manager.getFilePath(parent_dir, 'CalendarFiles')

    directory_manager.MakeDirectory(_main_dir)
        
    def CreateICSEvent(e_name, e_description, s_datetime, e_datetime,duration,
                    e_organizer_addr="", e_organizer_name="", e_organizer_role="",
                    e_location="", e_priority=5, rrule={}, tz='Asia/Singapore'):
        
        # Add subcomponents
        event = Event()
        event.add('name', e_name)
        event.add('summary', e_name) # serves as name for some calendars (Mac)
        event.add('description', e_description)

        event.add('dtstart', s_datetime)
        
        if rrule == {}: event.add('dtend', e_datetime)
        else: 
            event.add('dtend', e_datetime + timedelta(hours=duration))
            event.add('rrule', rrule)

        # Add the organizer
        organizer = vCalAddress(e_organizer_addr)
        
        # Add parameters of the event
        organizer.params['name'] = vText(e_organizer_name)
        organizer.params['role'] = vText(e_organizer_role)
        event['organizer'] = organizer
        event['location'] = vText(e_location)
        
        event['uid'] = uuid4()
        event.add('priority', e_priority)
        
        # Add the event to the calendar
        CalendarInterface._cal.add_component(event)
        f_name = f'{e_name}_{s_datetime}' # sanitization of name should already be done in the input
        f_name = TextProcessingManager.sanitize_raw_string(f_name)
        success = CalendarInterface.WriteToFile(file_name=f_name)
        if success: 
            CalendarInterface._cal.subcomponents.remove(event)
            return f_name
        else: 
            return None

    def WriteToFile(file_name=None)->bool:
        try:
            file_name = CalendarInterface._default_ics_file if file_name == None else file_name
            dir_to_open = CalendarInterface._main_dir

            directory_manager.WriteFile(dir_to_open, f'{file_name}.ics', CalendarInterface._cal.to_ical(), 'wb')
            return True
        except Exception as e:
            logging.error(f'FAILED TO WRITE {file_name}.ics TO {dir_to_open} because {e}')
            return False
    
    def ReadICSFile(file_name=None):
        file_name = CalendarInterface._default_ics_file if file_name == None else file_name
        dir_to_open = CalendarInterface._main_dir

        e = directory_manager.ReadFile(dir_to_open, f'{file_name}.ics', 'rb')
        ecal = icalendar.Calendar.from_ical(e)
        return ecal
    
    def getICSFilePath(file_name=None)->Path:
        file_name = CalendarInterface._default_ics_file if file_name == None else file_name
        dir_to_open = CalendarInterface._main_dir

        return directory_manager.getFilePath(dir_to_open, f'{file_name}.ics')
    
    def DeleteICSFilesInDir(dir: Path) ->bool:
        opt = directory_manager.DeleteFilesInDir(dir, 'ics')
        return opt

    def AppendStartTime(input:dict):
        time_slots = []
        time_slots.append(input['Start_Time'])
        time_slots.append(input['End_Time'])

        ics_s_date = TextProcessingManager.ProcessDateToICSFormat(input['Start_Date'])
        ics_e_date = TextProcessingManager.ProcessDateToICSFormat(input['End_Date'])
        ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
        ics_s, ics_e = TextProcessingManager.ProcessICS(ics_s_date, ics_e_date, ics_time)

        input['Start_Time_ICS'] = ics_s
        input['End_Time_ICS'] = ics_e