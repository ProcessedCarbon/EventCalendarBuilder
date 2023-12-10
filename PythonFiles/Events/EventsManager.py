from Managers.ErrorConfig import ErrorCodes
from pathlib import Path
import os
import Managers.DirectoryManager as directory_manager
from Managers.DateTimeManager import DateTimeManager
from Managers.TextProcessing import TextProcessingManager

class Event:
    def __init__(self, 
                 id:str, 
                 name:str, 
                 location:str, 
                 s_date:str, 
                 e_date:str,
                 start_time:str, 
                 end_time:str,
                 platform='Default',
                 recurring='None') -> None:
        
        self.id = id
        self.name = name
        self.location = location
        self.s_date = s_date
        self.e_date = e_date
        self.start_time = start_time
        self.end_time = end_time
        self.platform = platform
        self.recurring = recurring
    
    def getId(self)->str:
        return self.id
        
    def getName(self)->str:
        return self.name
        
    def getLocation(self)->str:
        return self.location
        
    def get_S_Date(self)->str:
        return self.s_date

    def get_E_Date(self)->str:
        return self.e_date
        
    def getStart_Time(self)->str:
        return self.start_time
        
    def getEnd_Time(self)->str:
        return self.end_time
    
    def getPlatform(self)->str:
        return self.platform

    def getRecurring(self)->str:
        return self.recurring

    def getEventDict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "location" : self.location,
            "s_date" : self.s_date,
            "e_date" : self.e_date,
            "start_time" : self.start_time,
            "end_time" : self.end_time,
            "platform" : self.platform,
            'recurring':self.recurring
        }
    
    def setId(self, id:str):
        self.id = id

    def setName(self, name:str):
        self.name = name
        
    def setLocation(self, location:str):
        self.location = location
        
    def set_S_Date(self, date:str):
        self.s_date = date
    
    def set_E_Date(self, date:str):
        self.e_date = date
        
    def setStart_Time(self, start_time:str):
        self.start_time = start_time
        
    def setEnd_Time(self, end_time:str):
        self.end_time = end_time
    
    def setPlatform(self, platform:str):
        self.platform = platform
    
    def setRecurring(self, recur:str):
        self.recurring = recur

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

    def CreateEventObj(name:str, 
                    location:str, 
                    s_date:str, 
                    e_date:str,                       
                    start_time:str, 
                    end_time:str,
                    platform='Default',
                    id='None',
                    recurring='None'):
        
        return Event(id=id,
                     name=name,
                     location=location,
                     s_date=s_date,
                     e_date=e_date,
                     start_time=start_time,
                     end_time=end_time,
                     platform=platform,
                     recurring=recurring)
        
    def PrintEvents(events : dict):
        event = events['object']
        print("------------------------------------------------------------------------------")
        print('id:', event.id)
        print("event: ", event.name)
        print("location: ", event.location)
        print("start_date: ", event.s_date)
        print("end_date: ", event.e_date)
        print("start_time: ", event.start_time)
        print("end_time: ", event.end_time)
        print('recurring:', event.recurring)
    
    def ClearEvents():
        EventsManager.events = []
    
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
                                                s_date=d['s_date'],
                                                e_date=d['e_date'],
                                                start_time=d['start_time'],
                                                end_time=d['end_time'],
                                                platform=d['platform'],
                                                recurring=d['recurring'])
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
    
    def RemoveFromEventDB(id:str, target=None)->bool:
        if target == None:
            ErrorCodes.PrintCustomError("MISSING DB TARGET")
            return False
        
        print(f'target_id: {id}')
        for e in target:
            if e['id'] == id:
                print(f'found: {e["id"]}')
                target.remove(e)
                return True
            
        print("TARGET NOT FOUND!")
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
                    if len(time) > 0: n_time = TextProcessingManager.ProcessTime(time_text=str(time))
                    else: n_time = [DateTimeManager.getCurrentTime()]

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

                    n_event = EventsManager.CreateEventObj(id=event_count,
                                                            name=event['EVENT'],
                                                            location=event["LOC"],
                                                            s_date=start_date,
                                                            e_date=start_date,
                                                            start_time=start_time,
                                                            end_time=end_time)
                    #print(vars(n_event))
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
                
                n_event = EventsManager.CreateEventObj(id=event_count,
                                                    name=event['EVENT'],
                                                    location=event["LOC"],
                                                    s_date=start_date,
                                                    e_date=end_date,
                                                    start_time=start_time,
                                                    end_time=end_time,
                                                    recurring=recurring)
                #print(vars(n_event))
                EventsManager.AddEventToEventDB(n_event, EventsManager.events)
                event_count += 1
        return EventsManager.events