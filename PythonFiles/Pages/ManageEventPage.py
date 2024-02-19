import logging

from Pages.Page import Page
from GUI.GUIInterface import GUIInterface
from Events.EventsManager import EventsManager
from GUI.EventCard import EventCard

class ManageEventPage(Page):
    def __init__(self, max_col=3, card_gap=10):   
        self.max_col = max_col  
        self.card_gap = card_gap 
        self.cards = {} 
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Title of page
        label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        label.grid(row=0, column=1)

        # Frame to hold all EventCards
        self.content_frame = GUIInterface.CreateScrollableFrame(self.page)
        self.content_frame.grid(row=1, column=1, sticky='nsew')

        # Clears the content and local events json of content_frame
        # Yet to remove the events scheduled on their respective calendar platform
        clear_events_json_btn = GUIInterface.CreateButton(on_click=self.Clear, 
                                                        text='Clear',
                                                        width=self.page.winfo_width() * 0.1)  
        clear_events_json_btn.grid(row=2, column=1)   
    
    def OnEntry(self):
        self.UpdateGUI()

    def UpdateGUI(self):
        # Create GUI only if there is data
        if len(EventsManager.events_db) > 0:

            # Create a grid in the content_frame for each scheduled event
            GUIInterface.CreateGrid(self.content_frame, rows=([1] * len(EventsManager.events_db)), cols=[1])

            for index, data in enumerate(EventsManager.events_db):
                # Pass details into GUI Events Card
                # Create Card under the scrollable content frame
                card = EventCard(self.content_frame, 
                                row=index, 
                                col=0, 
                                event_details=data, 
                                gap=self.card_gap,
                                index=index,
                                remove_cb=self.RemoveCard)
                #self.cards.append(card)
                self.cards[index] = card
    
    def RemoveCard(self, key):
        #print(self.cards)
        if key in self.cards:
            success = self.cards[key].Destroy()
            if success:
                del self.cards[key]
                self.content_frame.update()
                #print(f"SUCCESSFUL REMOVAL OF PANEL {key}")
                logging.info(f"SUCCESSFUL REMOVAL OF PANEL {key}")
            else: 
                #print(f"FAILED TO REMOVE PANEL {key}")
                logging.info(f"FAILED TO REMOVE PANEL {key}")

    def Clear(self):
        EventsManager.ClearEventsJSON() # clear events json
        for c in self.cards: self.cards[c].Destroy() # remove card GUIs