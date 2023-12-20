from Pages.Page import *
from Calendar.CalendarInterface import CalendarInterface
from GUI.EventDetailsPanel import EventDetailsPanel
from Events.EventsManager import EventsManager
from Pages.MiniPage import MiniPage

from math import ceil

class SchedulePage(Page):
    def __init__(self):
        self.details_panels = {}
        self.details_panels_frame = None
        self.panels = 0
        self.max_panel_per_page = 5
        self.current_page = None
        self.page_buttons = 0
        self.pages = {}
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Back Button
        button = GUIInterface.CreateButton(text="<", on_click=lambda:self.BackButton(0), width=50)
        button.grid(row=0, column=0, sticky='nw')

        # Title
        title = GUIInterface.CreateLabel(text="Schedule", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n')

        # Details
        self.details_panel_frame = GUIInterface.CreateScrollableFrame(self.page)
        self.details_panel_frame.grid(row=1, column=1, sticky='nsew')
        details_panel_frame_r = [1]
        details_panel_frame_c = [1]
        GUIInterface.CreateGrid(self.details_panel_frame, 
                                rows=details_panel_frame_r,
                                cols=details_panel_frame_c)
        
        # Page Buttons
        tmp = GUIInterface.current_frame
        self.page_button_frame = GUIInterface.CreateFrame(self.page, fg_color='blue')
        self.page_button_frame.grid(row=2, column=1, sticky='nsew')
        GUIInterface.current_frame = tmp

        # Create Event Button
        create_event = GUIInterface.CreateButton(on_click=self.CreateEventButton, text='Create')
        create_event.grid(row=3, column=1)

    def OnExit(self):
        self.ResetDetails()

    def OnEntry(self):
        if len(self.details_panels) > 0: self.ResetDetails()
        
        num_events = len(EventsManager.events)
        if num_events > 0:
            self.PopulateDetails(EventsManager.events)
            self.Update()
            EventsManager.ClearEvents()

    def PopulateDetails(self, events:list[dict]):
        self.current_page = None
        for index, event in enumerate(events):
            if self.panels % 5 == 0 or self.current_page == None: self.current_page = self.current_page = self.NewPage()
            detail_panel = EventDetailsPanel(parent=self.current_page.getPage(),
                                             event=event['object'],
                                             remove_cb=self.RemovePanel,
                                             key=index,
                                             row=self.current_page.getSize(), 
                                             column=0, 
                                             sticky='nsew')
            self.current_page.Queue(detail_panel)
            self.current_page.getPage().update()
            self.details_panels[index] = detail_panel
            self.panels += 1

    def ResetDetails(self):
        #print(f"Details panels: {self.details_panels}")
        for panel in self.details_panels:
            self.details_panels[panel].Reset()
            self.details_panels[panel].Destroy()
        self.details_panels={}
    
    def Update(self):
        for panel in self.details_panels:
            self.details_panels[panel].UpdateInputFields()
    
    def RemovePanel(self, key):
        if key in self.details_panels:
            self.details_panels[key].Destroy()
            del self.details_panels[key]
            self.details_panel_frame.update()
            print(f"SUCCESSFUL REMOVAL OF PANEL {key}")

    def BackButton(self, page:int=0):
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)
        PageManager.SwitchPages(page)

    def CreateEventButton(self):
        try:
            if self.panels % 5 == 0: 
                self.current_page = self.NewPage()
            empty_event = EventsManager.CreateEventObj(id=self.panels,
                                                        name='',
                                                        location='',
                                                        s_date='',
                                                        e_date='',
                                                        start_time='',
                                                        end_time='')
            detail_panel = EventDetailsPanel(parent=self.current_page.getPage(),
                                            event=empty_event,
                                            remove_cb=self.RemovePanel,
                                            key=self.panels,
                                            row=self.current_page.getSize(), 
                                            column=0, 
                                            sticky='nsew')
            self.current_page.Queue(detail_panel)
            self.current_page.getPage().update()
            self.details_panels[self.panels] = detail_panel
            self.panels += 1
            self.details_panel_frame.update()
        except Exception as e:
            ErrorCodes.PrintCustomError(e)
    
    def NewPage(self):
        page = MiniPage(size=self.max_panel_per_page,
                        parent=self.details_panel_frame)
        tmp = GUIInterface.current_frame
        self.page_buttons += 1
        GUIInterface.current_frame = self.page_button_frame
        GUIInterface.CreateGrid(self.page_button_frame, 
                                rows=[1],
                                cols=[1] * self.page_buttons)

        for i in range(self.page_buttons):
            self.pages[i] = page
            page_button = GUIInterface.CreateButton(text=str(i+1), on_click=page.SwitchTo)
            page_button.grid(row=0, column=i, padx=5)
        GUIInterface.current_frame = tmp
        self.details_panel_frame.update()
        return page