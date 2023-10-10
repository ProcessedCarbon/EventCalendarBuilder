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
    event_json = 'events'
    
    events = []
    events_db = []

    try:
        local_events_dir.mkdir(parents=True, exist_ok=False)
    except:
        print("EVENTS DIR ALREADY EXISTS")

    def __init__(self) -> None:
        pass

    def UpdateEventDict(id:int, update:Event)->bool:
        try:
            if len(EventsManager.events) > 0:
                EventsManager.events = [update if i["id"] == id else i for i in EventsManager.events]
            else:
                EventsManager.events.append(update)
            return True
        except Exception as e:
            ErrorCodes.PrintCustomError(e)
            return False
    
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

    def RemoveEvent(id:int):
        for event in EventsManager.events:
            if event.getId() == id:
                EventsManager.events.remove(event)
                return
            
        ErrorCodes.PrintCustomError("EVENT NOT FOUND")
    
    def SendEventsToEventsDB(event_list:list[Event]):
        try:
            eventList = [x for x in event_list if x not in EventsManager.events_db]
            EventsManager.events_db.extend(eventList)

            with open(Path(os.path.join(EventsManager.local_events_dir, f'{EventsManager.event_json}.json')), 'w') as file:
                for e in EventsManager.events_db:
                    json.dump(e, file)

        except Exception as e:
            ErrorCodes.PrintCustomError(e)

    def UpdateEventsDB():
        try:
            EventsManager.SendEventsToEventsDB(EventsManager.events)
            EventsManager.ClearEvents()
        except Exception as e:
            ErrorCodes.PrintCustomError(e)

    def AddEvent(event:Event):
        event_dict = event.getEventDict()
        event_dict['object'] = event
        EventsManager.events.append(event_dict)