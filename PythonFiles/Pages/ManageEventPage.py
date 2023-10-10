from Pages.Page import Page
from GUI.GUIInterface import GUIInterface
from Events.EventsManager import EventsManager
import os
import json
from Managers.ErrorConfig import ErrorCodes
import Managers.DirectoryManager as directory_manager

class ManageEventPage(Page):
    def __init__(self):        
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        label.grid(row=0, column=1)

        content_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        content_frame.grid(row=1, column=1, sticky='nsew')

        #scheduled_data = self.GetScheduledData()
        scheduled_data = directory_manager.ReadJSON(EventsManager.local_events_dir, EventsManager.event_json)
        
        if scheduled_data != None:
            pass
    
    # Given the data, create the UI for the events
    def CreateScheduledEventGUI(self, scheduled_data):
        if scheduled_data == None:
            return
        for data in scheduled_data:
            # Pass details into GUI Events Card

            # Create Card under the scrollable content frame
            pass
