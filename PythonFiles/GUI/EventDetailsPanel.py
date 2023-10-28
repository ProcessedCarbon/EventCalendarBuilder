from GUI.GUIInterface import GUIInterface
from Managers.ErrorConfig import getParamValFromKwarg
from Events.EventsManager import Event
from Events.EventsManager import EventsManager
from Managers.TextProcessing import TextProcessingManager

# Calendar Intefaces
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
from Calendar.CalendarInterface import CalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
from Calendar.Outlook.OutlookInterface import OutlookEvent

from sys import platform
import os
import subprocess

class EventDetailsPanel:
    def __init__(self, parent, event:Event, remove_callback,index:int, gap:int=10, **grid_params):
        self.gap = gap
        self.parent = parent
        self.grid_params = grid_params

        self.details_entries = {}
        self.filled = False
        self.details_frame = None
        self.event = event
        self.remove_callback = remove_callback
        self.index = index
        self.rows = 9

        self.GUI()
        
    def GUI(self):
        tmp_frame = GUIInterface.current_frame
        self.details_frame = GUIInterface.CreateFrame(self.parent, fg_color='green')

        # Find grid in parent to place this event panel
        row = getParamValFromKwarg("row", self.grid_params, default=0)
        column = getParamValFromKwarg("column", self.grid_params, default=0)
        sticky = getParamValFromKwarg("sticky", self.grid_params, default='nsew')
        self.details_frame.grid(row=row, 
                                column=column, 
                                sticky=sticky, 
                                padx=self.gap, 
                                pady=self.gap,
                                ipadx=self.gap)
        
        # Rows
        for i in range(self.rows):
            self.details_frame.rowconfigure(i, weight=1)
        
        # Columns
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.columnconfigure(1, weight=10)
        self.details_frame.columnconfigure(2, weight=1)

        self.details_frame.update() # update values from resized UI

        # GUI Attributes
        detail_entry_width = self.details_frame.winfo_width() * 0.7

        # GUI
        remove_btn = GUIInterface.CreateButton(on_click=self.OnRemove, text='X', width=50)
        remove_btn.grid(row=0, column=2, pady=10)

        e_frame, e_entry = self.CreateEntryField(detail_entry_width, 
                                                 entryname="Event", 
                                                 placeholder_text='Title')
        e_frame.grid(row=1, column=1,sticky='nsew', pady=self.gap)

        desp_frame, desp_entry = self.CreateEntryField(detail_entry_width, 
                                                       entryname="Description", 
                                                       placeholder_text='Description')
        desp_frame.grid(row=2, column=1, sticky='nsew',pady=self.gap)

        priorities = ["1", "2", "3", "4", "5"]
        prio_frame = self.CreateDropdownField(values=priorities, entryname="Priority")
        prio_frame.grid(row=3, column=1, sticky='nsew',pady=self.gap)

        l_frame, l_entry = self.CreateEntryField(detail_entry_width, 
                                                 entryname="Location", 
                                                 placeholder_text='Location')
        l_frame.grid(row=4, column=1, sticky='nsew',pady=self.gap)

        d_frame, d_entry = self.CreateEntryField(detail_entry_width, 
                                                 entryname="Date", 
                                                 entry_state='disabled', 
                                                 placeholder_text='YYYY-MM-DD')
        d_frame.grid(row=5, column=1,sticky='nsew',pady=self.gap)
        d_entry.bind('<1>', lambda event, entry=d_entry: self.PickDate(entry))

        st_frame, st_entry = self.CreateEntryField(detail_entry_width, 
                                                   entryname="Start Time", 
                                                   placeholder_text="HH:MM:SS")
        st_frame.grid(row=6, column=1,sticky='nsew',pady=self.gap)

        et_frame, et_entry = self.CreateEntryField(detail_entry_width,
                                                   entryname="End Time", 
                                                   placeholder_text="HH:MM:SS")
        et_frame.grid(row=7, column=1,sticky='nsew',pady=self.gap)

        calendars_frame = self.CreateDropdownField(values=["Default", "Google", 'Outlook'], entryname="Calendar")
        calendars_frame.grid(row=8, column=1, sticky='nsew',pady=self.gap)

        schedule_btn = GUIInterface.CreateButton(on_click=self.ScheduleEvent, text='Schedule')
        schedule_btn.grid(row=9, column=1, sticky='nsew')

        GUIInterface.SetCurrentFrame(tmp_frame)

    def UpdateEventWithDetails(self):
        details = self.getCurrentInputFieldsInfo()
        self.event.setName(details['Event'])
        self.event.setLocation(details['Location'])
        self.event.setDate(details['Date'])
        self.event.setStart_Time(details['Start_Time'])
        self.event.setEnd_Time(details['End_Time'])

    def UpdateInputFields(self):
        GUIInterface.UpdateEntry(self.details_entries["Event"], self.event.getName())
        GUIInterface.UpdateEntry(self.details_entries["Location"], self.event.getLocation())
        GUIInterface.UpdateEntry(self.details_entries["Date"], self.event.getDate())
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], self.event.getStart_Time())
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], self.event.getEnd_Time())
        self.filled = True

    def getEmptyInputFieldsCount(self)->int:
        count = 0
        for entry in self.details_entries:
            t = self.details_entries[entry].get()
            if t == "" or t == " ":
                count += 1
        return count
    
    def Reset(self):
        self.filled = False

        GUIInterface.UpdateEntry(self.details_entries["Event"], "")
        GUIInterface.UpdateEntry(self.details_entries["Location"], "")
        GUIInterface.UpdateEntry(self.details_entries["Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], "")

    def Destroy(self):
        self.details_frame.destroy()
    
    # Create GUI
    def CreateEntryField(self, width:int, entryname:str, entry_state='normal', placeholder_text=None):
        key = self.ConvertEntryNameToKey(entryname)
        e_frame, e_label, e_entry = GUIInterface.CreateEntryWithLabel(label= entryname + ":",
                                                                      entry_width=width, 
                                                                      entry_state=entry_state,
                                                                      placeholder_text=placeholder_text)
        self.details_entries[key] = e_entry
        return e_frame, e_entry

    def CreateDropdownField(self, values:list[str], entryname:str):
        key = self.ConvertEntryNameToKey(entryname)
        dropdown_frame, dropdown_label, dropdown_box = GUIInterface.CreateOptionMenuWithLabel(label=entryname +":", dropdown=values)
        self.details_entries[key] = dropdown_box
        return dropdown_frame
    
    def ConvertEntryNameToKey(self, name:str):
        return name.replace(" ", "_")
    
    def getCurrentInputFieldsInfo(self)->dict:
        details = {}
        for detail in self.details_entries:
            details[detail] = self.details_entries[detail].get()
        return details
    
    def getEvent(self):
        return self.event
    
    def OnRemove(self):
        EventsManager.RemoveEvent(id=self.event.getId())
        self.remove_callback(self.index)
        self.Destroy()
    
    def PickDate(self, entry):
        date_window, cal, submit_btn = GUIInterface.CreateDateWindow()
        submit_btn.configure(command=lambda:self.GrabDate(entry, cal.get_date(), date_window))

    def GrabDate(self, entry, date:str, window):
        GUIInterface.UpdateEntry(entry, date)
        window.destroy()

    def ScheduleEvent(self):
        print("SCHEDULE CLICKED!")

        # Check if all required fields are filled
        if self.getEmptyInputFieldsCount() == self.rows:
            print("Required field is empty!")
            return
        
        input = self.getCurrentInputFieldsInfo()

        # Handle missing or incorrect input for time fields
        if input['Start_Time'] == "":
            print(f'Missing Start Time field for {input["Event"].upper()}[{input["Date"]}]')
            return
        elif input['End_Time'] == "":
            print(f'Missing End Time field for {input["Event"].upper()}[{input["Date"]}]')
            return
        elif TextProcessingManager.CheckStringFormat(input['Start_Time']) == None:
            print(f'Incorrect Start Time provided for {input["Event"].upper()}[{input["Date"]}]')
            return
        elif TextProcessingManager.CheckStringFormat(input['End_Time']) == None:
            print(f'Incorrect End Time provided for {input["Event"].upper()}[{input["Date"]}]')
            return
        
        # If no isses then create ics file
        # Process datetime to ics calendar format
        time_slots = []
        time_slots.append(input['Start_Time'])
        time_slots.append(input['End_Time'])

        ics_date = TextProcessingManager.ProcessDateToICSFormat(input['Date'])
        ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
        ics_s, ics_e = TextProcessingManager.ProcessICS(ics_date, ics_time)

        input['Start_Time_ICS'] = ics_s
        input['End_Time_ICS'] = ics_e

        # Scheduling
        calendar = input['Calendar']
        if calendar == 'Default':
            self.ScheduleDefault(input)

            # No clash checking done for default yet
            # No need to add platform to event object as its default
            EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
            EventsManager.WriteEventDBToJSON()
            self.Destroy()
        elif calendar == 'Google':
            success = self.ScheduleGoogleCalendar(input)
            if success:
                self.event.setPlatform('Google')
                EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
                EventsManager.WriteEventDBToJSON()
                self.Destroy()
        elif calendar == 'Outlook':
            success = self.ScheduleOutlookCalendar(input)
            if success:
                self.event.setPlatform('Outlook')
                EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
                self.Destroy()

    # Right now can only handle 1 event only 
    def ScheduleDefault(self, event):
        if platform == 'darwin':
            filename = self.CreateICSFileFromInput(event)
            file = CalendarInterface.getICSFilePath(filename)
            subprocess.run(['open', file])
        else:
            filename = self.CreateICSFileFromInput(event)
            file = CalendarInterface.getICSFilePath(filename)
            os.startfile(file)

    def ScheduleGoogleCalendar(self, event)->bool:
        
        filename = self.CreateICSFileFromInput(event)
        events = GoogleCalendarInterface.Parse_ICS(filename)
        for e in events:
            scheduled = GoogleCalendarInterface.ScheduleCalendarEvent(googleEvent=e)
            if scheduled == False:
                return False
        return True

    def ScheduleOutlookCalendar(self, event)->bool:
        filename = self.CreateICSFileFromInput(event)
        outlook_event = outlook_interface.parse_ics(filename)
        # Cannot pass an entire dictionary as a param 
        scheduled = outlook_interface.send_flask_req(req='create_event', 
                                                     json_data={'event': outlook_event.event})
        if scheduled == False:
            return False
        return True
    
    # Creates ICS files to be parsed 
    # 1 ICS = should have 1 VEVENT
    # returns names of file created
    def CreateICSFileFromInput(self, event)->str:
        desp = event["Description"]
        priority = int(event["Priority"])
        location = event["Location"]
        title = event["Event"]
        ics_s = event["Start_Time_ICS"]
        ics_e = event["End_Time_ICS"]

        # Create ICS File
        CalendarInterface.CreateICSEvent(e_name=title,
                                        e_description=desp,
                                        s_datetime=ics_s,
                                        e_datetime=ics_e,
                                        e_location=location,
                                        e_priority=int(priority))
        
        file_name = f'{title}_{ics_s}'
        CalendarInterface.WriteToFile(file_name)
        return file_name