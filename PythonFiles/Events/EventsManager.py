from Managers.ErrorConfig import ErrorCodes

class Event:
    def __init__(self, id:int, name:str, location:str, date:str, start_time:str, end_time:str) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.start_time = start_time
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