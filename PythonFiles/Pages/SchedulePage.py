from Pages.Page import *
from GUI.MainAppWindow import MainAppWindow
from Calendar.CalendarInterface import CalendarInterface
from Managers.TextProcessing import TextProcessingManager
from Managers.DateTimeManager import DateTimeManager
from GUI.EventDetailsPanel import EventDetailsPanel
from Events.EventsManager import EventsManager
from Events.EventsManager import Event
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface

from sys import platform
import os
import subprocess

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

        # Schedule Button
        schedue_btn = GUIInterface.CreateButton(text="Schedule",on_click=self.ScheduleEvents)
        schedue_btn.grid(row=2, column=1, sticky='s', pady=10)

        # Title
        title = GUIInterface.CreateLabel(text="Schedule", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n')

        # Details
        self.details_panel_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        self.details_panel_frame.grid(row=1, column=1, sticky='nsew')

    def OnExit(self):
        self.ResetDetails()
        self.UpdateEventsDB()

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
            panel.UpdateDetails()
    
    def CheckDetailsForDateTimeClash(self, details:list)->bool:
        n = len(details)
        for i in range(n):
            for j in range (i+1, n):
                if j > n:
                    break
                
                start_1 = str(details[i]["Start_Time_ICS"])
                end_1 = str(details[i]['End_Time_ICS'])

                start_2 = str(details[j]["Start_Time_ICS"])
                end_2 = str(details[j]['End_Time_ICS'])

                if DateTimeManager.hasDateTimeClash(start_1, end_1, start_2, end_2):
                    ErrorCodes.PrintCustomError(f'{details[i]["Event"]} AND {details[j]["Event"]} HAS CLASH')
                    return True
        return False

    def ScheduleEvents(self):
        # Check if all inputs are empty
        for panel in self.details_panels:
            # If a panel is empty reject 
            if panel.getEmptyDetailCount() == EventDetailsPanel.num_details:
                print("Empty panel found!")
                return
                         
            details = panel.getDetails()

            # Panel has missing Start or End time reject
            if details['Start_Time'] == "" or details['End_Time'] == "":
                print(f'Missing Start or End time for {details["Event"].upper()}[{details["Date"]}]')
                return
        
        # Create ICS Event per EventDetailPanel
        to_schedule = []
        for panel in self.details_panels:
            details = panel.getDetails()

            # Process datetime to ics calendar format
            time_slots = []
            time_slots.append(details['Start_Time'])
            time_slots.append(details['End_Time'])

            ics_date = TextProcessingManager.ProcessDateToICSFormat(details['Date'])
            ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
            ics_s, ics_e = TextProcessingManager.ProcessICS(ics_date, ics_time)
            
            details['Start_Time_ICS'] = ics_s
            details['End_Time_ICS'] = ics_e

            to_schedule.append(details)
        
        if self.CheckDetailsForDateTimeClash(to_schedule):
            return
        
        self.ScheduleDefault(to_schedule)
        #self.ScheduleGoogleCalendar(to_schedule)
        self.UpdateEventsDB()
    
    # Creates ICS files to be parsed
    def CreateICSFile(self, to_schedule:list[dict], split_ics=False):
        for schedule in to_schedule:
                #Retrieve params from input
                desp = schedule["Description"]
                priority = int(schedule["Priority"])
                location = schedule["Location"]
                event = schedule["Event"]
                ics_s = schedule["Start_Time_ICS"]
                ics_e = schedule["End_Time_ICS"]

                # Create ICS File
                CalendarInterface.CreateICSEvent(e_name=event,
                                                e_description=desp,
                                                s_datetime=ics_s,
                                                e_datetime=ics_e,
                                                e_location=location,
                                                e_priority=int(priority))
                
                # Immediately write to a file 
                CalendarInterface.WriteToFile(f'{event}_({ics_s})') if split_ics else None

        CalendarInterface.WriteToFile() if split_ics == False else None

        
    def DeleteDetailPanel(self, index:int):
        del self.details_panels[index]

    def UpdateEventsDB(self):
        try:
            EventsManager.SendEventsToEventsDB(EventsManager.events)
            EventsManager.ClearEvents()
        except Exception as e:
            ErrorCodes.PrintCustomError(e)

    # Right now can only handle 1 event only 
    def ScheduleDefault(self, to_schedule:list[dict]):
        if platform == "linux":
            self.CreateICSFile(to_schedule)
            filename = CalendarInterface.getICSFilePath()
            subprocess.run(['xdg-open', filename])
            pass
        elif platform == 'darwin':
            self.CreateICSFile(to_schedule)
            filename = CalendarInterface.getICSFilePath()
            subprocess.run(['open', filename])
        else:
            self.CreateICSFile(to_schedule)
            path = CalendarInterface.getICSFilePath()
            os.startfile(path)

    def ScheduleGoogleCalendar(self, to_schedule:list[dict]):
        self.CreateICSFile(to_schedule)
        events = GoogleCalendarInterface.Parse_ICS(CalendarInterface._default_ics_file)
        for e in events:
            GoogleCalendarInterface.ScheduleCalendarEvent(googleEvent=e)

    def BackButton(self, page:int=0):
        CalendarInterface.ClearICSFilesInDir(CalendarInterface._main_dir)
        CalendarInterface.ClearICSFilesInDir(CalendarInterface._split_dir)

        PageManager.SwitchPages(page)