import icalendar
from icalendar import Calendar, Event, vCalAddress, vText
from pathlib import Path
import os
import glob
import Managers.DirectoryManager as directory_manager

class CalendarInterface:
    _cal = Calendar()
    
    # Directories
    parent_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()
    _main_dir = Path(os.path.join(parent_dir, 'CalendarFiles'))
    _split_dir = Path(os.path.join(_main_dir, 'Splitted'))
    _default_ics_file = 'to_schedule'

    try:
        _main_dir.mkdir(parents=True, exist_ok=False)
        _split_dir.mkdir(parents=True, exist_ok=False)
    except:
        print("CALENDAR DIR ALREADY EXISTS")
    
    def __init__(self):
        # Some properties are required to be compliant
        CalendarInterface._cal.add('prodid', '-//My calendar product//example.com//')
        CalendarInterface._cal.add('version', '2.0')
        pass
        
    def CreateICSEvent(e_name, e_description, s_datetime, e_datetime, 
                    e_organizer_addr="", e_organizer_name="", e_organizer_role="",
                    e_location="", e_priority=5):
        
        # Add subcomponents
        event = Event()
        event.add('name', e_name)
        event.add('description', e_description)
        event.add('dtstart', s_datetime)
        event.add('dtend', e_datetime)
        
        # Add the organizer
        organizer = vCalAddress(e_organizer_addr)
        
        # Add parameters of the event
        organizer.params['name'] = vText(e_organizer_name)
        organizer.params['role'] = vText(e_organizer_role)
        event['organizer'] = organizer
        event['location'] = vText(e_location)
        
        event['uid'] = '2022125T111010/272356262376@example.com'
        event.add('priority', e_priority)

        # Not handling attendees for now
        # attendee = vCalAddress('MAILTO:rdoe@example.com')
        # attendee.params['name'] = vText('Richard Roe')
        # attendee.params['role'] = vText('REQ-PARTICIPANT')
        # event.add('attendee', attendee, encode=0)
        
        # attendee = vCalAddress('MAILTO:jsmith@example.com')
        # attendee.params['name'] = vText('John Smith')
        # attendee.params['role'] = vText('REQ-PARTICIPANT')
        # event.add('attendee', attendee, encode=0)
        
        # Add the event to the calendar
        CalendarInterface._cal.add_component(event)

    def WriteToFile(file_name=None, main=True)->bool:
        try:
            file_name = CalendarInterface._default_ics_file if file_name == None else file_name
            dir_to_open = CalendarInterface._main_dir if main else CalendarInterface._split_dir
            
            directory_manager.WriteFile(dir_to_open, f'{file_name}.ics', CalendarInterface._cal.to_ical(), 'wb')
            return True
        except:
            print(f'FAILED TO WRITE {file_name}.ics TO {dir_to_open}')
            return False
    
    def ReadICSFile(file_name=None, main=True):
        file_name = CalendarInterface._default_ics_file if file_name == None else file_name
        dir_to_open = CalendarInterface._main_dir if main else CalendarInterface._split_dir

        e = directory_manager.ReadFile(dir_to_open, f'{file_name}.ics', 'rb')
        ecal = icalendar.Calendar.from_ical(e)
        for component in ecal.walk():
            if component.name == "VEVENT":
                print(component.get("name"))
                print(component.get("description"))
                print(component.get("organizer"))
                print(component.get("location"))
                print(component.decoded("dtstart"))
                print(component.decoded("dtend"))
        return ecal

    # def getICSFile(file_name=None, main=True):
    #     file_name = CalendarInterface._default_ics_file if file_name == None else file_name
    #     dir_to_open = CalendarInterface._main_dir if main else CalendarInterface._split_dir

    #     e = open(Path(os.path.join(dir_to_open, f'{file_name}.ics')), 'rb')
    #     ecal = icalendar.Calendar.from_ical(e.read())
    #     return ecal
    
    def getICSFilePath(file_name=None, main=True)->Path:
        file_name = CalendarInterface._default_ics_file if file_name == None else file_name
        dir_to_open = CalendarInterface._main_dir if main else CalendarInterface._split_dir

        return Path(os.path.join(dir_to_open, f'{file_name}.ics'))

    def getAllICSFilePathsFromDir(dir:Path)->list[Path]:
        paths = glob.glob(f'{dir}/*.ics')
        return paths
    
    def DeleteICSFilesInDir(dir:Path)->bool:
        try:
            files = glob.glob(f"{dir}/*.ics")
            for f in files:
                os.unlink(f)
            print(f'DELETE ALL FILES IN {dir} SUCCESSFULLY!')
            return True
        except:
            print(f'FAILED TO DELETE FILES IN {dir}')
            return False

    # def CreateNewDir(dir_name:str, parent_dir:Path)->Path:
    #     try:
    #         new_dir = Path(os.path.join(parent_dir, dir_name))
    #         new_dir.mkdir(parents=True, exist_ok=False)
    #         return new_dir
    #     except:
    #         print("CALENDAR DIR ALREADY EXISTS")
    #         return new_dir
