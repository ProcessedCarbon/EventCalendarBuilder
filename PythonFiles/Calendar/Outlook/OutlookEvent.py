# Format:
# https://learn.microsoft.com/en-us/graph/api/calendar-post-events?view=graph-rest-1.0&tabs=http
class OutlookEvent():
    def __init__(self, 
                name:str, location:str,  dtstart:str, rrule:str, description: str,
                dtend:str, tzstart:str, tzend:str, isonline=False) -> None:
        
        self.name = name
        self.location = location
        self.dtstart = dtstart
        self.dtend = dtend
        self.tzstart = tzstart
        self.tzend = tzend
        self.isonline = isonline
        self.rrule = rrule
        self.description = description
        
        self.event = {
            "subject": name,
            "body": {
                "contentType": "HTML",
                "content": description
            },
            "start": {
                "dateTime": dtstart,
                "timeZone": tzstart
            },
            "end": {
                "dateTime": dtend,
                "timeZone": tzend
            },
            "location":{
                "displayName":location
            },
            "isOnlineMeeting": isonline,
            }
        self.reccurence_pattern = self.getRecurrencePatternFromRRULE(rrule=self.rrule)
        if self.reccurence_pattern != {}: self.event['recurrence'] = self.reccurence_pattern

    
    def get_name(self):
        return self.name
    
    def get_location(self):
        return self.location
    
    def get_dtstart(self):
        return self.dtstart
    
    def get_dtend(self):
        return self.dtend
    
    def get_tzstart(self):
        return self.tzstart
    
    def get_tzend(self):
        return self.tzend
    
    def get_isonline(self):
        return self.isonline
    
    def get_rrule(self):
        return self.rrule
    
    def get_descriptuon(self):
        return self.description

    # Assuming RRULES come in the following format
    # FREQ=DAILY;INTERVAL=10;COUNT=5 
    def getRecurrencePatternFromRRULE(self, rrule:str):
        if rrule == '': return {}
        split = rrule.split(';')
        rule_dict = {}
        # Convert each split into a single dictionary
        for s in split:
            split_s = s.split('=')
            key = split_s[0]
            val = split_s[1]
            rule_dict[key] = val
        
        freq = rule_dict['FREQ'].lower() if 'FREQ' in rule_dict else ''
        end_y = rule_dict['UNTIL'][:4]
        end_m = rule_dict['UNTIL'][4:6] 
        end_d = rule_dict['UNTIL'][6:8] 
        end_date = f'{end_y}-{end_m}-{end_d}'

        s_date = self.dtstart.split('T')[0]
        return {
            "pattern": {
                "type": freq,
                "interval": 1
            },
            "range": {
                "type": "endDate",
                "startDate": s_date,
                "endDate": end_date
            }
        }