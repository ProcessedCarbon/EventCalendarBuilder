from Pages.Page import Page
from GUI.GUIInterface import GUIInterface
from Events.EventsManager import EventsManager
import Managers.DirectoryManager as directory_manager

from GUI.EventCard import EventCard

class ManageEventPage(Page):
    def __init__(self, max_col=3, card_gap=10):   
        self.max_col = max_col  
        self.card_gap = card_gap  
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Title of page
        label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        label.grid(row=0, column=1)

        # Frame to hold all EventCards
        content_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        content_frame.grid(row=1, column=1, sticky='nsew')

        # Get event data from JSON
        scheduled_data = directory_manager.ReadJSON(EventsManager.local_events_dir, EventsManager.event_json)
        
        # Create a grid in the content_frame for each scheduled event
        GUIInterface.CreateGrid(content_frame, rows=([1] * len(scheduled_data)), cols=[1])

        # Create GUI only if there is data
        if scheduled_data != None:
            for index, data in enumerate(scheduled_data):
                # Pass details into GUI Events Card
                # Create Card under the scrollable content frame
                EventCard(content_frame, 
                          row=index, 
                          col=0, 
                          event_details=data, 
                          gap=self.card_gap)        