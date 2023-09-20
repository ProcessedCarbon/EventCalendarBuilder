from Pages.Page import *
from GUI.MainAppWindow import MainAppWindow
from NER.NERInterface import NERInterface
from Calendar.CalendarInterface import CalendarInterface
from Managers.TextProcessing import TextProcessingManager
from Managers.DateTimeManager import DateTimeManager
from GUI.EventDetailsPanel import EventDetailsPanel
from Events.EventsManager import EventsManager
from Events.EventsManager import Event
from math import ceil

class SchedulePage(Page):
    def __init__(self):
        self.details_panels = []
        self.details_panels_max_column = 3
        self.entry_width = MainAppWindow.app_width * 0.5
        self.details_panels_frame = None
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Back Button
        button = GUIInterface.CreateButton(text="<", on_click=lambda:PageManager.SwitchPages(0), width=50)
        button.grid(row=0, column=0, sticky='nw')

        # Schedule Button
        schedue_btn = GUIInterface.CreateButton(text="Schedule",on_click=self.CreateICSUsingEntities)
        schedue_btn.grid(row=2, column=1, sticky='s', pady=10)

        # Title
        title = GUIInterface.CreateLabel(text="Schedule", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n')

        # Details
        self.details_panel_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        self.details_panel_frame.grid(row=1, column=1, sticky='nsew')

    def OnExit(self):
        self.ResetDetails()

    def OnEntry(self):
        if len(self.details_panels) > 0:
            self.ResetDetails()

        num_events = len(EventsManager.events)
        if num_events > 0:
            self.PopulateDetails(num_events)
            self.Update()

    def PopulateDetails(self, num_events):
        detail_rows = ceil(num_events / self.details_panels_max_column)
        rows = [1] * detail_rows
        cols = [1] * self.details_panels_max_column
        GUIInterface.CreateGrid(self.details_panel_frame, rows=rows, cols=cols)
        row_at = 0
        for i in range(num_events):
            count = i % self.details_panels_max_column
            if count == 0 and i != 0:
                row_at += 1
            detail_panel = EventDetailsPanel(self.details_panel_frame, 
                                             self.entry_width, 
                                             row=row_at, 
                                             column=count, 
                                             sticky='nsew')
            self.details_panels.append(detail_panel)

    def ResetDetails(self):
        for panel in self.details_panels:
            panel.Reset()
            panel.Destroy()
        self.details_panels=[]

    def UpdatePanel(self, panel:EventDetailsPanel, event:Event):
        panel.UpdateDetails(Event=event.name, 
                            Location=event.location, 
                            Date=event.date, 
                            Start_Time=event.start_time, 
                            End_Time=event.end_time)
    
    def Update(self):
        if len(EventsManager.events) > 0:
            for panel in self.details_panels:
                event = EventsManager.events.pop(0)
                self.UpdatePanel(panel, event)
    
    def CheckDetailsForDateTimeClash(self, details:list)->bool:
        n = len(details)
        for i in range(n):
            for j in range (i+1, n):
                if j > n:
                    break
                
                start_1 = str(details[i]["Start_Time_ICS"])
                end_1 = str(details[i]['End_Time_ICS'])

                start_2 = str(details[j]["Start_Time_ICS"])
                end_2 = str(details[j]['End_Time_ICS'])

                if DateTimeManager.hasDateTimeClash(start_1, end_1, start_2, end_2):
                    self.Prompt(f'{details[i]["Event"]} and {details[j]["Event"]} has clash')
                    return True
        return False

    def CreateICSUsingEntities(self):
        # Check if all inputs are empty
        for panel in self.details_panels:
            if panel.getEmptyDetailCount() == EventDetailsPanel.num_details:
                print("Empty panel found!")
                return
        
        # Create ICS Event per EventDetailPanel
        to_schedule = []
        for panel in self.details_panels:
            details = panel.getDetails()

            # Process datetime to ics calendar format
            time_slots = []
            time_slots.append(details['Start_Time'])
            time_slots.append(details['End_Time'])

            ics_date = TextProcessingManager.ProcessDateToICSFormat(details['Date'])
            ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
            ics_s, ics_e = TextProcessingManager.ProcessICS(ics_date, ics_time)
            
            details['Start_Time_ICS'] = ics_s
            details['End_Time_ICS'] = ics_e

            to_schedule.append(details)
        
        if self.CheckDetailsForDateTimeClash(to_schedule):
            return
        
        for schedule in to_schedule:
            #Retrieve params from input
            desp = schedule["Description"]
            priority = int(schedule["Priority"])
            location = schedule["Location"]
            event = schedule["Event"]
            ics_s = schedule["Start_Time_ICS"]
            ics_e = schedule["End_Time_ICS"]

            # Create ICS File
            CalendarInterface.CreateICSEvent(e_name=event,
                                            e_description=desp,
                                            s_datetime=ics_s,
                                            e_datetime=ics_e,
                                            e_location=location,
                                            e_priority=int(priority))
        CalendarInterface.WriteToFile()
        CalendarInterface.ReadICSFile()
        
        

