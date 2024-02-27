from tkinter import messagebox
from math import ceil
from customtkinter import *

from Pages.Page import *
from Calendar.CalendarInterface import CalendarInterface
from GUI.EventDetailsPanel import EventDetailsPanel
from Events.EventsManager import EventsManager

class SchedulePage(Page):
    def __init__(self):
        self.details_panels = {}
        self.details_panels_max_column = 3
        self.details_panels_frame = None
        self.max_panels = 10
        self.panels = 0
        GUIInterface.root.bind("<Button-1>",self.on_click)
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        # Back Button
        button = GUIInterface.CreateButton(text="<", on_click=lambda:self.BackButton(0), width=50)
        button.grid(row=0, column=0, sticky='nw')

        # Title
        title = GUIInterface.CreateLabel(text="Schedule", font=("Bold", 20))
        title.grid(row=0, column=1, sticky='n')

        # Details
        self.details_panel_frame = GUIInterface.CreateScrollableFrame(self.page)
        self.details_panel_frame.grid(row=1, column=1, sticky='nsew')
        GUIInterface.CreateGrid(self.details_panel_frame, 
                                rows=[1],
                                cols=[1])

        # Create Event Button
        create_event = GUIInterface.CreateButton(on_click=self.CreateEventButton, text='Create')
        create_event.grid(row=2, column=1)

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
                                            dup_cb=self.on_click,
                                            key=index,
                                            row=index, 
                                            column=0, 
                                            sticky='nsew')
            self.details_panels[index] = detail_panel
            self.panels += 1

    def ResetDetails(self):
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
            logging.info(f"[{__name__}] SUCCESSFUL REMOVAL OF PANEL {key}")

    def changeOrder(self, widget1,widget2,initial):
        target=widget1.grid_info()
        widget1.grid(row=initial['row'],column=initial['column'])
        widget2.grid(row=target['row'],column=target['column'])

    def on_click(self, event):
        widget=event.widget
        print(widget) 
        if isinstance(widget,CTkCanvas):
            start=(event.x,event.y)
            grid_info=widget.grid_info()
            widget.bind("<B1-Motion>",lambda event:self.drag_motion(event,widget,start))
            widget.bind("<ButtonRelease-1>",lambda event:self.drag_release(event,widget,grid_info))
        else:
            GUIInterface.root.unbind("<ButtonRelease-1>")

    def drag_motion(self, event,widget,start):
        x = widget.winfo_x()+event.x-start[0]
        y = widget.winfo_y()+event.y-start[1] 
        widget.lift()
        widget.place(x=x,y=y)

    def drag_release(self, event,widget,grid_info):
        widget.lower()
        x,y=GUIInterface.root.winfo_pointerxy()
        target_widget=GUIInterface.root.winfo_containing(x,y)
        if isinstance(target_widget,CTkFrame):
            self.changeOrder(target_widget,widget,grid_info)
        else:
            widget.grid(row=grid_info['row'],column=grid_info['column'])

    def BackButton(self, page:int=0):
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)
        PageManager.SwitchPages(page)

    def CreateEventButton(self):
        try:
            if self.panels == self.max_panels:
                messagebox.showwarning(title='Max Event Reached!', message=f'Max event panels of {self.max_panels} reached.')
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
