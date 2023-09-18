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
            
    def CreateICSUsingEntities(self):

        # Check if all inputs are empty
        for panel in self.details_panels:
            if panel.getEmptyDetailCount() == EventDetailsPanel.num_details:
                print("Empty panel found!")
                return
        
        print(self.details_panels)
        # Create ICS Event per EventDetailPanel
        for panel in self.details_panels:
            details_entries = panel.getDetailEntries()
            # Retrieve params from input
            date = details_entries["Date"].get()
            s_time = details_entries["Start_Time"].get()
            e_time = details_entries["End_Time"].get()
            desp = details_entries["Description"].get()
            priority = int(details_entries["Priority"].get())
            location = details_entries["Location"].get()
            event = details_entries["Event"].get()

            time_slots = []
            time_slots.append(s_time)
            time_slots.append(e_time)

            # Convert date and time to ics format
            ics_date = TextProcessingManager.ProcessDateToICSFormat(date)
            ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
            ics_s, ics_e = TextProcessingManager.ProcessICS(ics_date, ics_time)

            # Create ICS File
            CalendarInterface.CreateICSEvent(e_name=event,
                                            e_description=desp,
                                            s_datetime=ics_s,
                                            e_datetime=ics_e,
                                            e_location=location,
                                            e_priority=int(priority))
        CalendarInterface.WriteToFile()
        CalendarInterface.ReadICSFile()
        
        

