import icalendar
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import glob

class CalendarInterface:
    _cal = Calendar()
    
    # Directories
    parent_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()
    _main_dir = Path(os.path.join(parent_dir, 'CalendarFiles'))
    _split_dir = Path(os.path.join(_main_dir, 'Splitted'))
    _default_ics_file = 'to_schedule'

    def __init__(self):
        # Some properties are required to be compliant
        CalendarInterface._cal.add('prodid', '-//My calendar product//example.com//')
        CalendarInterface._cal.add('version', '2.0')
        pass

    def CreateICSEvent(e_name:str, e_description:str, s_datetime:datetime, e_datetime:datetime, 
                    e_organizer_addr:str="", e_organizer_name:str="", e_organizer_role:str="",
                    e_location:str="", e_priority:int=5):
        
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

    def WriteToFile(file_name:str, dir_name:Path)->bool:
        try:
            # Check if directory exists, if it does not, create it.
            new = CalendarInterface.CreateNewDir(dir_name)
            f = open(Path(os.path.join(new, f'{file_name}.ics')), 'wb')
            f.write(CalendarInterface._cal.to_ical())
            f.close()
            print(f'SUCCESSFULLY WRITTEN {file_name}.ics TO {new}')
            return True
        except:
            print(f'FAILED TO WRITE {file_name}.ics TO {new}')
            return False
    
    def ReadICSFile(file_name:str, dir:Path):
        e = open(Path(os.path.join(dir, f'{file_name}.ics')), 'rb')
        ecal = icalendar.Calendar.from_ical(e.read())
        for component in ecal.walk():
            if component.name == "VEVENT":
                print(component.get("name"))
                print(component.get("description"))
                print(component.get("organizer"))
                print(component.get("location"))
                print(component.decoded("dtstart"))
                print(component.decoded("dtend"))
            e.close()

    def getICSFile(file_name:str, dir:Path):
        e = open(Path(os.path.join(dir, f'{file_name}.ics'), 'rb'))
        ecal = icalendar.Calendar.from_ical(e.read())
        return ecal
    
    def getICSFilePath(file_name:str, dir:Path)->Path:
        return Path(os.path.join(dir, f'{file_name}.ics'))

    def getAllICSFilePathsFromDir(dir:Path)->list[Path]:
        paths = glob.glob(f'{dir}/*.ics')
        return paths
    
    def ClearICSFilesInDir(dir:Path)->bool:
        try:
            files = glob.glob(f"{dir}/*.ics")
            for f in files:
                os.unlink(f)
            print(f'CLEARED ALL FILES IN {dir} SUCCESSFULLY!')
            return True
        except:
            print(f'FAILED TO CLEAR FILES IN {dir}')
            return False

    def CreateNewDir(dir_name:str)->Path:
        try:
            new_dir = Path(os.path.join(CalendarInterface.parent_dir, dir_name))
            new_dir.mkdir(parents=True, exist_ok=False)
            return new_dir
        except:
            print("CALENDAR DIR ALREADY EXISTS")
            return new_dir
