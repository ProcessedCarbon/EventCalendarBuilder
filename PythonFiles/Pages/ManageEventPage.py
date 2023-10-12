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

        label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        label.grid(row=0, column=1)

        content_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        content_frame.grid(row=1, column=1, sticky='nsew')

        # Get event data from JSON
        scheduled_data = directory_manager.ReadJSON(EventsManager.local_events_dir, EventsManager.event_json)
        
        # Create GUI only if there is data
        if scheduled_data != None:
            if scheduled_data == None:
                return
        
            row_count = 0
            col_count = 0
            for data in scheduled_data:
                # Pass details into GUI Events Card
                # Create Card under the scrollable content frame
                EventCard(content_frame, 
                          row=row_count, 
                          col=col_count, 
                          event_details=data, 
                          gap=self.card_gap)
                
                col_count += 1
                if col_count == self.max_col:
                    row_count += 1
                    col_count = 0
        