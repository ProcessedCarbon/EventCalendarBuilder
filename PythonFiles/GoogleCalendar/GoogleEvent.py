class GoogleEvent:
    def __init__(self, event: str, location: str, time_start: str, time_end: str, date_start: str, date_end: str, timezone: str, colorId=1):
        start_datetime = self.CreateGoogleDateTimeFormat(date=date_start, time=time_start)
        end_datetime = self.CreateGoogleDateTimeFormat(date=date_end, time=time_end)

        self.event = {
            "summary" : event,
            "location" : location,
            "description" : "Test description",
            "colorId" : colorId,
            "start" : {
                "dateTime" : start_datetime,
                "timeZone" : timezone
            },
            "end" : {
                "dateTime" : end_datetime,
                "timeZone" : timezone
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
    
    def CreateGoogleDateTimeFormat(self, date: str, time: str):
        return date + "T" + time
    
