from Pages.Page import *
from Calendar.CalendarInterface import CalendarInterface
from GUI.EventDetailsPanel import EventDetailsPanel
from Events.EventsManager import EventsManager
from Events.EventsManager import Event

from math import ceil

class SchedulePage(Page):
    def __init__(self):
        self.details_panels = []
        self.details_panels_max_column = 3
        self.details_panels_frame = None
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Back Button
        button = GUIInterface.CreateButton(text="<", on_click=lambda:self.BackButton(['to_schedule'], 0), width=50)
        button.grid(row=0, column=0, sticky='nw')

        # Title
        title = GUIInterface.CreateLabel(text="Schedule", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n')

        # Details
        self.details_panel_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        self.details_panel_frame.grid(row=1, column=1, sticky='nsew')

    def OnExit(self):
        self.ResetDetails()
        EventsManager.UpdateEventsDB()

    def OnEntry(self):
        if len(self.details_panels) > 0:
            self.ResetDetails()
        
        num_events = len(EventsManager.events)
        if num_events > 0:
            self.PopulateDetails(EventsManager.events)
            self.Update()

    def PopulateDetails(self, events:list[Event]):
        n = len(events)
        detail_rows = ceil(n / self.details_panels_max_column)
        rows = [1] * detail_rows
        cols = [1] * self.details_panels_max_column
        GUIInterface.CreateGrid(self.details_panel_frame, rows=rows, cols=cols)
        row_at = 0
        for index, event in enumerate(events):
            count = index % self.details_panels_max_column
            if count == 0 and index != 0:
                row_at += 1
            detail_panel = EventDetailsPanel(parent=self.details_panel_frame,
                                             event=event,
                                             remove_callback=self.DeleteDetailPanel,
                                             index=index, 
                                             row=row_at, 
                                             column=count, 
                                             sticky='nsew')
            self.details_panels.append(detail_panel)

    def ResetDetails(self):
        for panel in self.details_panels:
            panel.Reset()
            panel.Destroy()
        self.details_panels=[]
    
    def Update(self):
        for panel in self.details_panels:
            panel.UpdateInputFields()
    
    # def CheckDetailsForDateTimeClash(self, details:list)->bool:
    #     n = len(details)
    #     for i in range(n):
    #         for j in range (i+1, n):
    #             if j > n:
    #                 break
                
    #             start_1 = str(details[i]["Start_Time_ICS"])
    #             end_1 = str(details[i]['End_Time_ICS'])

    #             start_2 = str(details[j]["Start_Time_ICS"])
    #             end_2 = str(details[j]['End_Time_ICS'])

    #             if DateTimeManager.hasDateTimeClash(start_1, end_1, start_2, end_2):
    #                 ErrorCodes.PrintCustomError(f'{details[i]["Event"]} AND {details[j]["Event"]} HAS CLASH')
    #                 return True
    #     return False
        
    def DeleteDetailPanel(self, index:int):
        del self.details_panels[index]

    def BackButton(self, page:int=0):
        CalendarInterface.ClearICSFilesInDir(CalendarInterface._main_dir)
        CalendarInterface.ClearICSFilesInDir(CalendarInterface._split_dir)

        PageManager.SwitchPages(page)