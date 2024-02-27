from tkinter import messagebox
from math import ceil
from uuid import uuid4
import copy

from Pages.Page import *
from Calendar.CalendarInterface import CalendarInterface
from GUI.EventDetailsPanel import EventDetailsPanel
from GUI.GUIConstants import MAX_EVENT_TITLE, EVENT_DETAILS_PANEL_ROW_GAP
from Events.EventsManager import EventsManager

class SchedulePage(Page):
    def __init__(self):
        self.details_panels = {}
        self.details_panels_max_column = 3
        self.details_panels_frame = None
        self.max_panels = 10
        self.panels = 0
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Back Button
        button = GUIInterface.CreateButton(text="<", on_click=lambda:self.BackButton(0), width=50)

        # Details
        self.details_panel_frame = GUIInterface.CreateScrollableFrame(self.page)
        GUIInterface.CreateGrid(self.details_panel_frame, 
                                rows=[1],
                                cols=[1])

        # Create Event Button
        create_event = GUIInterface.CreateButton(on_click=self.CreateEventButton, text='Create')

        # Grid elements
        button.grid(row=0, column=0, sticky='nw')
        self.details_panel_frame.grid(row=1, column=1, sticky='nsew')
        create_event.grid(row=2, column=1)

    def OnExit(self):
        self.ResetDetails()
        EventsManager.ClearEvents()

    def OnEntry(self):
        if len(self.details_panels) > 0: self.ResetDetails()
        
        num_events = len(EventsManager.events)
        if num_events > 0:
            self.PopulateDetails(EventsManager.events)

    def PopulateDetails(self, events:list[dict]):
        n = len(events)
        detail_rows = ceil(n / self.details_panels_max_column)
        GUIInterface.CreateGrid(self.details_panel_frame, rows=([1] * detail_rows), cols=[1])
        for index, event in enumerate(events):
            if self.panels == self.max_panels:
                messagebox.showwarning(title='Max Event Reached!', message=f'Max event panels of {self.max_panels} reached.')
                break
            detail_panel = EventDetailsPanel(parent=self.details_panel_frame,
                                            event=event['object'],
                                            remove_cb=self.RemovePanel,
                                            dup_cb=self.DuplicatePanel,
                                            key=index,
                                            row=index)
            self.details_panels[index] = detail_panel
            self.panels += 1
        
        self.Update()

    def ResetDetails(self):
        for panel in self.details_panels:
            self.details_panels[panel].Reset()
            self.details_panels[panel].Destroy()
        self.details_panels={}
        self.panels = 0
    
    def Update(self):
        for panel in self.details_panels:
            self.details_panels[panel].UpdateInputFields()
    
    def RemovePanel(self, key):
        if key in self.details_panels:
            self.details_panels[key].Destroy()
            del self.details_panels[key]
            self.details_panel_frame.update()
            logging.info(f"[{__name__}] SUCCESSFUL REMOVAL OF PANEL {key}")

    def DuplicatePanel(self, key):
        
        for panel in self.details_panels:
            self.details_panels[panel].UpdateEventWithDetails()

        for index, e in enumerate(EventsManager.events):
            event = e['object']
            if event.getId() == key:
                # Create a copy
                dup = e.copy()
                dup['object'] = copy.copy(e['object'])

                # Update params
                dup['object'].copy += 1
                e['object'].copy += 1 # update original as well
                dup['id'] = uuid4()
                if dup['name'].endswith(']'):
                    dup['name'] = dup['name'][:-4]
                dup['name'] = dup['name'] + f' [{dup["object"].getCopy()}]'
                dup['object'].setName(dup['name'])
                dup['object'].setId(dup['id'])

                # Insert in list
                first_slice = EventsManager.events[:index+1]
                second_slice = EventsManager.events[index+1:]
                first_slice.append(dup)
                first_slice.extend(second_slice)

                # Update list
                EventsManager.ClearEvents()
                EventsManager.events = first_slice

                # Re-create GUI
                self.ResetDetails()
                self.PopulateDetails(EventsManager.events)

    def BackButton(self, page:int=0):
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)
        PageManager.SwitchPages(page)

    def CreateEventButton(self):
        try:
            if self.panels == self.max_panels:
                messagebox.showwarning(title=MAX_EVENT_TITLE, message=f'Max event panels of {self.max_panels} reached.')
                return
            
            empty_event = EventsManager.CreateEventObj(id=self.panels,
                                                        name='',
                                                        location='',
                                                        s_date='',
                                                        e_date='',
                                                        start_time='',
                                                        end_time='')

            detail_panel = EventDetailsPanel(parent=self.details_panel_frame,
                                            event=empty_event,
                                            remove_cb=self.RemovePanel,
                                            key=self.panels,
                                            row=self.panels, 
                                            column=0, 
                                            sticky='nsew')
            
            self.details_panels[self.panels] = detail_panel
            self.panels += 1
            self.details_panel_frame.update()
        except Exception as e:
            logging.error(f"[{__name__}]: {e}")
