import icalendar
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz

class CalendarInterface:
    def __init__(self):
        self._cal = Calendar()
        parent_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
        self._calendar_file_dir = Path(os.path.join(parent_dir,"CalendarFiles"))
        print(self._calendar_file_dir)

        # Some properties are required to be compliant
        self._cal.add('prodid', '-//My calendar product//example.com//')
        self._cal.add('version', '2.0')
        pass

    def CreateICSEvent(self, e_name:str, e_description:str, e_date:datetime, e_dtend:datetime, 
                    e_organizer_addr:str="", e_organizer_name:str="", e_organizer_role:str="",
                    e_location:str="", e_priority:int=5):
        # Add subcomponents
        event = Event()
        event.add('name', e_name)
        event.add('description', e_description)
        event.add('dtstart', datetime(2022, 1, 25, 8, 0, 0, tzinfo=pytz.utc))
        event.add('dtend', datetime(2022, 1, 25, 10, 0, 0, tzinfo=pytz.utc))
        
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
        self._cal.add_component(event)

    def WriteToFile(self):
        try:
            self._calendar_file_dir.mkdir(parents=True, exist_ok=False)
        except:
            pass

        f = open(os.path.join(self._calendar_file_dir, 'example.ics'), 'wb')
        f.write(self._cal.to_ical())
        f.close()
    
    def ReadICSFile(self):
        e = open(os.path.join(self._calendar_file_dir, 'example.ics'), 'rb')
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

def BasicTest():
    cal_interface = CalendarInterface()
    cal_interface.CreateICSEvent()
    cal_interface.WriteToFile()
    cal_interface.ReadICSFile()

def main():
    BasicTest()
    pass

if __name__ == "__main__":
    main()