from Pages.Page import *
from NER.NERInterface import NERInterface
from Managers.TextProcessing import TextProcessingManager
from GUI.MainAppWindow import MainAppWindow
from Events.EventsManager import EventsManager
from Managers.DateTimeManager import DateTimeManager

class MainPage(Page):
    def __init__(self): 
        self.main_page_textbox = None
        super().__init__()
    
    def OnStart(self):
        rows = [1, 1, 1]
        cols = [1, 1, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Text box
        self.main_page_textbox = GUIInterface.CreateTextbox(width=MainAppWindow.app_width * 0.5, height=MainAppWindow.app_height * 0.5)
        self.main_page_textbox.grid(row=1, column=1, sticky='nsew')

        # Button
        button = GUIInterface.CreateButton(text="Submit", on_click=lambda:self.Submit(self.main_page_textbox))
        button.grid(row=2, column=1, stick='s', pady=10)
    
    def OnExit(self):
        if self.main_page_textbox != None:
            GUIInterface.ClearTextBox(self.main_page_textbox)
            return
        ErrorCodes.PrintCustomError("MISSING TEXTBOX REFERENCE")

    def Submit(self, textbox):
        success = self.ReadAndProcessText(textbox)
        
        if success:
            PageManager.SwitchPages(1) 

    def ReadAndProcessText(self,textbox)->bool:
        t = GUIInterface.RetrieveCurrentInputFromTextbox(textbox)

        if t == "" or t == " " or t == "\n":
            print("No text found!")
            return False
        
        t.strip("\n").strip()
        events = NERInterface.GetEntitiesFromText(text=t)

        # Process time and date using the same events list
        for i in range(len(events)):
            date_time = events[i]["DATE_TIME"].copy()
            if len(date_time) == 0:
                curr_date = DateTimeManager.getCurrentDate()
                formatted_date = curr_date.strftime("%Y-%m-%d")
                events[i]["DATE_TIME"] = {formatted_date : [DateTimeManager.getCurrentTime()]}
                date = formatted_date
            else:
                for d in date_time:
                    time = date_time[d]
                    date = TextProcessingManager.ProcessDate(date_text=str(d))
                    if len(time) > 0: n_time = TextProcessingManager.ProcessTime(time_text=str(time))
                    else: n_time = [DateTimeManager.getCurrentTime()]

                    events[i]["DATE_TIME"].pop(d)
                    if isinstance(date, list) and len(date) > 1: 
                        for o in date: events[i]["DATE_TIME"][o] = n_time
                    else: events[i]["DATE_TIME"][date] = n_time

            # Check how many dates event has, only create and end time if there is only
            # a single date else just treat that date pair as a range and sort them in ascending
            # Also handle the pairing of dates
            n = len(events[i]["DATE_TIME"])
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
            else: events[i]["DATE_TIME"] = dict(sorted(events[i]["DATE_TIME"].items()))

        # print("MID")
        # for e in events: print(e)

        print("------------------------------------------------------------------------------")
        print("Add to event manager list")
        for index, event in enumerate(events):
            # If more than 2 dates just ignore for now
            keys = list(events[index]['DATE_TIME'].keys())
            if len(keys) > 2:
                continue
        
            start_date = keys[0]
            end_date = start_date

            start_time = event['DATE_TIME'][start_date][0]
            end_time = start_time
            recurring = 'None'

            if len(keys) == 2: 
                print(f"start_{len(event['DATE_TIME'][keys[0]])}")
                print(f"end_{len(event['DATE_TIME'][keys[1]])}")
                end_date = keys[1]
                if len(event['DATE_TIME'][start_date]) == 2 and len(event['DATE_TIME'][end_date]) == 2:
                    if event['DATE_TIME'][start_date] == event['DATE_TIME'][end_date]:
                        recurring = 'Daily'
                        end_time = event['DATE_TIME'][end_date][1]
                else: end_time = event['DATE_TIME'][end_date][0]
            else:
                if len(event['DATE_TIME'][end_date]) > 1: end_time = event['DATE_TIME'][end_date][1]

            n_event = EventsManager.CreateEventObj(id=index,
                                                name=event['EVENT'],
                                                location=event["LOC"],
                                                s_date=start_date,
                                                e_date=end_date,
                                                start_time=start_time,
                                                end_time=end_time,
                                                recurring=recurring)
            #print(vars(n_event))
            EventsManager.AddEventToEventDB(n_event, EventsManager.events)
            print(EventsManager.events)
            # testing
            for event in EventsManager.events:
                EventsManager.PrintEvents(event)
            print("------------------------------------------------------------------------------")            
            print("Done!")
        return True