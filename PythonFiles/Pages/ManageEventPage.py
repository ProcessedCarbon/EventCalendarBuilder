import logging

from Pages.Page import Page
from GUI.GUIInterface import GUIInterface
from Calendar.CalendarInterface import CalendarInterface
from Events.EventsManager import EventsManager
from GUI.EventCard import EventCard
from Pages.PageConstants import AUTO_REMOVE_OLD_EVENTS
from Managers.DateTimeManager import DateTimeManager

class ManageEventPage(Page):
    def __init__(self):   
        self.cards = {} 
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Title of page
        self.label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))

        # Frame to hold all EventCards
        self.content_frame = GUIInterface.CreateScrollableFrame(self.page)

        # Auto Remove Old Events
        self.autoRemoveLabel =  GUIInterface.CreateLabel(text="Auto Remove Old Events from Manage Page:")
        self.autoRemoveSwitch = GUIInterface.CreateSwitch(text="", onvalue=1, offvalue=0, border_color='grey', command=self.autoRemoveSwitchValue)

        # Grid GUI
        self.label.grid(row=0, column=1)
        self.content_frame.grid(row=1, column=1, sticky='nsew')
        self.autoRemoveLabel.grid(row=2, column=1, sticky='nsew')
        self.autoRemoveSwitch.grid(row=3, column=1, sticky='nsew')

    def OnEntry(self):
        self.UpdateGUI()

        if AUTO_REMOVE_OLD_EVENTS:
            self.CheckExpiredEvents()
    
    def OnExit(self):
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)

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
                                event_details=data, 
                                index=index,
                                remove_cb=self.RemoveCard)
                self.cards[index] = card
    
    def RemoveCard(self, key, askBeforeDelete=True):
        if key in self.cards:
            success = self.cards[key].Destroy(askBeforeDelete)
            if success:
                del self.cards[key]
                self.content_frame.update()
                logging.info(f"SUCCESSFUL REMOVAL OF PANEL {key}")
            else: 
                logging.info(f"FAILED TO REMOVE PANEL {key}")

    def Clear(self):
        EventsManager.ClearEventsJSON() # clear events json
        for c in self.cards: self.cards[c].Destroy() # remove card GUIs

    def CheckExpiredEvents(self):
        if len(self.cards) <= 0:
            return
        
        cardsCopy = self.cards.copy()
        now_date = str(DateTimeManager.getDateTimeNow().date())
        now_time = str(DateTimeManager.getDateTimeNow().time()).split('.')[0]

        for c in cardsCopy:
            print(self.cards[c].event_details)
            end_date = cardsCopy[c].event_details['e_date']
            end_time = cardsCopy[c].event_details['end_time']

            isEventDateOver = DateTimeManager.CompareDates(now_date, str(end_date))
            isEventDateEquals = DateTimeManager.areDatesEqual(now_date, str(end_date))
            isEventTimeOver = DateTimeManager.CompareTimes(str(end_time), now_time)
            eventOver = True if isEventDateOver and (isEventDateEquals and isEventTimeOver or not isEventDateEquals) else False

            if not eventOver:
                return
            
            cardsCopy[c].RemoveCard(False)

        self.content_frame.update()