class GoogleEvent:
    def __init__(self, event: str, 
                 location: str, 
                 start_datetime: str, 
                 end_datetime: str, 
                 tzstart: str, 
                 tzend:str, 
                 colorId=1):
        
        self.event = {
            "summary" : event,
            "location" : location,
            "description" : "Test description",
            "colorId" : colorId,
            "start" : {
                "dateTime" : start_datetime,
                "timeZone" : tzstart
            },
            "end" : {
                "dateTime" : end_datetime,
                "timeZone" : tzend
            },
            # "recurrence" : [
            #     "RRULE:FREQ=DAILY;COUNT=2"
            # ],
            # "attendees" : [
            #     {"email":"nonexistantemail@mail.com"}
            # ]
        }

    def __repr__(self):
        return f"GoogleEvent(event='{self.event}')"
