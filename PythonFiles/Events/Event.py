from Calendar.CalendarConstants import DEFAULT_CALENDAR

class Event:
    def __init__(self, 
                id:str, 
                name:str, 
                location:str, 
                s_date:str, 
                e_date:str,
                start_time:str, 
                end_time:str,
                platform=DEFAULT_CALENDAR,
                recurring='None',
                description='') -> None:
        
        self.id = id
        self.name = name
        self.location = location
        self.s_date = s_date
        self.e_date = e_date
        self.start_time = start_time
        self.end_time = end_time
        self.platform = platform
        self.recurring = recurring
        self.description = description
    
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
    
    def getDescription(self)->str:
        return self.description

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
            'recurring':self.recurring,
            'description': self.description,
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
    
    def setDescription(self, desc: str):
        self.description = desc