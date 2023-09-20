from Managers.ErrorConfig import ErrorCodes

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
    events = []
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
    def PrintEvents(events : Event):
        print("------------------------------------------------------------------------------")
        print("event: ", events.name)
        print("location: ", events.location)
        print("date: ", events.date)
        print("start_time: ", events.start_time)
        print("end_time: ", events.end_time)
    
    def ClearEvents():
        EventsManager.events = []

    def RemoveEvent(id:int):
        for event in EventsManager.events:
            if event.getId() == id:
                EventsManager.events.remove(event)
                return
            
        ErrorCodes.PrintCustomError("EVENT NOT FOUND")