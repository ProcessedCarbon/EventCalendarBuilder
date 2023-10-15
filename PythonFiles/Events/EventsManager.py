from Managers.ErrorConfig import ErrorCodes
from pathlib import Path
import os
import Managers.DirectoryManager as directory_manager
import uuid

class Event:
    def __init__(self, 
                 id:str, 
                 name:str, 
                 location:str, 
                 date:str, 
                 start_time:str, 
                 end_time:str,
                 platform='Default') -> None:
        
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.platform = platform
    
    def getId(self)->str:
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
    
    def getPlatform(self)->str:
        return self.platform

    def getEventDict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "location" : self.location,
            "date" : self.date,
            "start_time" : self.start_time,
            "end_time" : self.end_time,
            "platform" : self.platform
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
    
    def setPlatform(self, platform:str):
        self.platform = platform
    
class EventsManager:
    # Directories
    parent_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()
    local_events_dir = Path(os.path.join(parent_dir, 'Local_Events'))
    event_json = 'events.json'
    
    # Temporary event list
    events = []

    # Only contains events that are scheduled by app
    events_db = []

    try:
        local_events_dir.mkdir(parents=True, exist_ok=False)
    except:
        print("EVENTS DIR ALREADY EXISTS")

    def CreateEventObj(id:int, 
                       name:str, 
                       location:str, 
                       date:str, 
                       start_time:str, 
                       end_time:str,
                       platform='Default'):
        
        return Event(id=f'{id}_{uuid.uuid4()}', # Done this way to reduce chances of UUID clashes
                     name=name,
                     location=location,
                     date=date,
                     start_time=start_time,
                     end_time=end_time,
                     platform=platform)
        
    def PrintEvents(events : dict):
        event = events['object']
        print("------------------------------------------------------------------------------")
        print('id:', event.id)
        print("event: ", event.name)
        print("location: ", event.location)
        print("date: ", event.date)
        print("start_time: ", event.start_time)
        print("end_time: ", event.end_time)
    
    def ClearEvents():
        EventsManager.events = []

    def RemoveEvent(id:str, target=None):
        if target == None:
            ErrorCodes.PrintCustomError("MISSING DB TARGET")
            return
        
        for event in target:
            e = event['object']
            if e.getId() == id:
                target.remove(event)
                return
            
        ErrorCodes.PrintCustomError("EVENT NOT FOUND")
    
    def UpdateEventsDB():
        '''
        Updates the local event db list by reading from the local events.json
        '''
        # Get event data from JSON
        data = directory_manager.ReadJSON(EventsManager.local_events_dir, EventsManager.event_json)
        if data == None:
            print("NO LOCALLLY SCHEDULED EVENTS")
            return
        
        for d in data:
            event = EventsManager.CreateEventObj(id=d['id'],
                                                name=d['name'],
                                                location=d['location'],
                                                date=d['date'],
                                                start_time=d['start_time'],
                                                end_time=d['end_time'],
                                                platform=d['platform'])
            EventsManager.AddEventToEventDB(event=event, target=EventsManager.events_db)

    # Send only those that are schedule
    def WriteEventDBToJSON():
        '''
        Writes events db to a local events.json file to store locally
        '''
        try:
            # eventList = [x for x in EventsManager.local_events if x not in EventsManager.events_db]
            # EventsManager.events_db.extend(eventList)

            db_copy = EventsManager.events_db.copy()

            # convert to json dumpable format
            for e in db_copy:
                    for key in e:
                        if type(e[key]) != str:
                            e[key] = str(e[key])

            # Create JSON file with events
            directory_manager.WriteJSON(EventsManager.local_events_dir, EventsManager.event_json, db_copy)

        except Exception as e:
            ErrorCodes.PrintCustomError(e)

    def AddEventToEventDB(event:Event, target=None):
        '''
        Takes in an event object and adds it to the target list in this class
        Works with the assumption that event db is updated
        '''
        if target == None:
            ErrorCodes.PrintCustomError("MISSING DB TARGET")
            return

        event_dict = event.getEventDict()
        event_dict['object'] = event
        target.append(event_dict)
    
    def ClearEventsJSON():
        directory_manager.WriteJSON(EventsManager.local_events_dir, EventsManager.event_json, content=None)