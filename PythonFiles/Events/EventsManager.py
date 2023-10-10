from Managers.ErrorConfig import ErrorCodes
from pathlib import Path
import os
import glob
import json

class Event:
    def __init__(self, id:int, name:str, location:str, date:str, start_time:str, end_time:str) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
    
    def getId(self)->int:
        return self.id
        
    def getName(self)->str:
        return self.name
        
    def getLocation(self)->str:
        return self.location
        
    def getDate(self)->str:
        return self.date
        
    def getStart_Time(self)->str:
        return self.start_time
        
    def getEnd_Time(self)->str:
        return self.end_time
    
    def getEventDict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "location" : self.location,
            "date" : self.date,
            "start_time" : self.start_time,
            "end_time" : self.end_time,
        }
        
    def setName(self, name:str):
        self.name = name
        
    def setLocation(self, location:str):
        self.location = location
        
    def setDate(self, date:str):
        self.date = date
        
    def setStart_Time(self, start_time:str):
        self.start_time = start_time
        
    def setEnd_Time(self, end_time:str):
        self.end_time = end_time
        
    
class EventsManager:
    # Directories
    parent_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()
    local_events_dir = Path(os.path.join(parent_dir, 'Local_Events'))
    event_json = 'events.json'
    
    # Temporary event list
    events = []
    app_scheduled_events = []

    # Only contains events that are scheduled by app
    events_db = []

    try:
        local_events_dir.mkdir(parents=True, exist_ok=False)
    except:
        print("EVENTS DIR ALREADY EXISTS")

    def __init__(self) -> None:
        pass
    
    def CreateEventObj(name:str, location:str, date:str, start_time:str, end_time:str):
        return Event(id=EventsManager.getCurrentId(),
                     name=name,
                     location=location,
                     date=date,
                     start_time=start_time,
                     end_time=end_time)

    def getCurrentId():
        n = len(EventsManager.events)
        return n - 1 if n != 0 else 0
    
        # Prints entity per event in list
    
    def PrintEvents(events : dict):
        event = events['object']
        print("------------------------------------------------------------------------------")
        print("event: ", event.name)
        print("location: ", event.location)
        print("date: ", event.date)
        print("start_time: ", event.start_time)
        print("end_time: ", event.end_time)
    
    def ClearEvents():
        EventsManager.events = []
        EventsManager.app_scheduled_events = []

    def RemoveEvent(id:int):
        for event in EventsManager.events:
            e = event['object']
            if e.getId() == id:
                EventsManager.events.remove(event)
                return
            
        ErrorCodes.PrintCustomError("EVENT NOT FOUND")
    
    # Send only those that are schedule
    def SendEventsToEventsDB():
        try:
            eventList = [x for x in EventsManager.app_scheduled_events if x not in EventsManager.events_db]
            EventsManager.events_db.extend(eventList)
    
            with open(Path(os.path.join(EventsManager.local_events_dir, EventsManager.event_json)), 'w') as file:
                db_copy = EventsManager.events_db.copy()
                
                # convert to json dumpable
                for e in db_copy:
                    for key in e:
                        if type(e[key]) != str:
                            e[key] = str(e[key])

                # Json Dump
                json.dump(db_copy, file)
            file.close()

        except Exception as e:
            ErrorCodes.PrintCustomError(e)

    def UpdateEventsDB():
        try:
            EventsManager.SendEventsToEventsDB()
            EventsManager.ClearEvents()
        except Exception as e:
            ErrorCodes.PrintCustomError(e)

    def AddEvent(event:Event, target=None):
        target = EventsManager.events if target == None else target

        event_dict = event.getEventDict()
        event_dict['object'] = event
        target.append(event_dict)