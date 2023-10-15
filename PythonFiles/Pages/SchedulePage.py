from Pages.Page import *
from Calendar.CalendarInterface import CalendarInterface
from GUI.EventDetailsPanel import EventDetailsPanel
from Events.EventsManager import EventsManager

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
        button = GUIInterface.CreateButton(text="<", on_click=lambda:self.BackButton(0), width=50)
        button.grid(row=0, column=0, sticky='nw')

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
            self.PopulateDetails(EventsManager.events)
            self.Update()

    def PopulateDetails(self, events:list[dict]):
        n = len(events)
        detail_rows = ceil(n / self.details_panels_max_column)
        GUIInterface.CreateGrid(self.details_panel_frame, rows=([1] * detail_rows), cols=[1])
        for index, event in enumerate(events):
            detail_panel = EventDetailsPanel(parent=self.details_panel_frame,
                                             event=event['object'],
                                             remove_callback=self.DeleteDetailPanel,
                                             index=index, 
                                             row=index, 
                                             column=0, 
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
        
    def DeleteDetailPanel(self, index:int):
        del self.details_panels[index]

    def BackButton(self, page:int=0):
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._split_dir)

        PageManager.SwitchPages(page)