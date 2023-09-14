from Pages.Page import *
from GUI.MainAppWindow import MainAppWindow
from NER.NERInterface import NERInterface
from Calendar.CalendarInterface import CalendarInterface
from Managers.TextProcessing import TextProcessingManager
from Managers.DateTimeManager import DateTimeManager
from GUI.EventDetailsPanel import EventDetailsPanel
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
        NERInterface.ClearEvents()
        self.ResetDetails()

    def OnEntry(self):
        if len(self.details_panels) > 0:
            self.ResetDetails()

        num_events = len(NERInterface.events)
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

    def UpdatePanel(self, panel:EventDetailsPanel, event_dict:dict):
            time_list = event_dict["TIME"]
            if len(time_list) < 2:
                new_time = DateTimeManager.AddToTime(time_list[0], hrs=1)
                time_list.append(new_time)

            event = str(event_dict["EVENT"])
            location = event_dict["LOC"]
            date = event_dict["DATE"]
            start_time = time_list[0]
            end_time = time_list[1]
            
            panel.UpdateDetails(Event=event, 
                                Location=location, 
                                Date=date, 
                                Start_Time=start_time, 
                                End_Time=end_time)
    
    def Update(self):
        if len(NERInterface.events) > 0:
            for panel in self.details_panels:
                event = NERInterface.events.pop(0)
                self.UpdatePanel(panel, event)

            NERInterface.ClearEvents()

    def CreateICSUsingEntities(self):

        # Check if all inputs are empty
        for panel in self.details_panels:
            if panel.getEmptyDetailCount() == EventDetailsPanel.num_details:
                print("Empty panel found!")
                return
            
        # Create ICS Event per EventDetailPanel
        for panel in self.details_panels:
            # Retrieve params from input
            date = panel.details_entries["Date"].get()
            s_time = panel.details_entries["Start_Time"].get()
            e_time = panel.details_entries["End_Time"].get()
            desp = panel.details_entries["Description"].get()
            priority = int(self.details_entries["Priority"].get())
            location = panel.details_entries["Location"].get()
            event = panel.details_entries["Event"].get()

            time_slots = []
            time_slots.append(s_time)
            time_slots.append(e_time)

            # Convert date and time to ics format
            ics_date = TextProcessingManager.ProcessDateToICSFormat(date)
            ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
            ics_time_s, ics_time_e = TextProcessingManager.ProcessICS(ics_date, ics_time)

            # Create ICS File
            CalendarInterface.CreateICSEvent(e_name=event,
                                            e_description=desp,
                                            s_datetime=ics_time_s,
                                            e_datetime=ics_time_e,
                                            e_location=location,
                                            e_priority=int(priority))
        CalendarInterface.WriteToFile()
        CalendarInterface.ReadICSFile()



        
        
        

