from tkinter import messagebox
import pytz
import logging
from customtkinter import *

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import MISSING_INPUT_TITLE, EVENT_DETAILS_PANEL_ROWS, SUCCESS_TITLE, EVENT_DETAILS_PANEL_DETAIL_GAP, EVENT_DETAILS_PANEL_ROW_GAP, EVENT_DETAILS_PANEL_ENTRY_WIDTH_MODIFIER
from Events.Event import Event
from Events.EventsManager import EventsManager
from Managers.TextProcessing import TextProcessingManager
from Calendar.CalendarConstants import DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR
import GUI.PopupManager as popup_mgr

class EventDetailsPanel:
    def __init__(self, parent, event:Event, remove_cb, dup_cb, row, key:int):
        self.parent = parent
        self.row = row

        self.details_entries = {}
        self.details_frame = None
        self.event = event
        self.key = key
        self.remove_cb = remove_cb
        self.dup_cb = dup_cb

        self.GUI()
        
    def GUI(self):
        tmp_frame = GUIInterface.current_frame
        self.details_frame = GUIInterface.CreateFrame(self.parent, 
                                                    fg_color=GUIInterface.color_palette['CTkFrame']['border_color'][0])

        # Find grid in parent to place this event panel
        self.details_frame.grid(row=self.row, 
                                column=0, 
                                sticky='nsew', 
                                padx=EVENT_DETAILS_PANEL_ROW_GAP, 
                                pady=EVENT_DETAILS_PANEL_ROW_GAP,
                                ipadx=EVENT_DETAILS_PANEL_ROW_GAP)
        
        # Rows
        for i in range(EVENT_DETAILS_PANEL_ROWS):
            self.details_frame.rowconfigure(i, weight=1)
        
        # Columns
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.columnconfigure(1, weight=10)
        self.details_frame.columnconfigure(2, weight=1)

        self.details_frame.update() # update values from resized UI

        # GUI Attributes
        detail_entry_width = self.details_frame.winfo_width() * EVENT_DETAILS_PANEL_ENTRY_WIDTH_MODIFIER

        # GUI
        remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(self.key), text='X', width=50)
        remove_btn.grid(row=0, column=1, pady=10, sticky='e')

        dup_btn = GUIInterface.CreateButton(on_click=lambda:self.dup_cb(self.event.getId()), text='+', width=40)
        dup_btn.grid(row=0, column=2, pady=10, padx=10, sticky='e')

        e_frame, e_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Event", 
                                                placeholder_text='Title')
        e_frame.grid(row=1, column=1,sticky='nsew', pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        desp_frame, desp_entry = self.CreateEntryField(detail_entry_width, 
                                                    entryname="Description", 
                                                    placeholder_text='Description')
        desp_frame.grid(row=2, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        l_frame, l_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Location", 
                                                placeholder_text='Location')
        l_frame.grid(row=3, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        s_d_frame, s_d_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Start Date", 
                                                entry_state='disabled', 
                                                placeholder_text='YYYY-MM-DD')
        s_d_entry.bind('<1>', lambda event, entry=s_d_entry: self.PickDate(entry))
        s_d_frame.grid(row=4, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        e_d_frame, e_d_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="End Date", 
                                                entry_state='disabled', 
                                                placeholder_text='YYYY-MM-DD')
        e_d_entry.bind('<1>', lambda event, entry=e_d_entry: self.PickDate(entry))
        e_d_frame.grid(row=5, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        st_frame, st_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Start Time", 
                                                placeholder_text="HH:MM:SS")
        st_frame.grid(row=6, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        et_frame, et_entry = self.CreateEntryField(detail_entry_width,
                                                entryname="End Time", 
                                                placeholder_text="HH:MM:SS")
        et_frame.grid(row=7, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        
        schedule_btn = GUIInterface.CreateButton(on_click=self.ScheduleEvent, text='Schedule')
        schedule_btn.grid(row=10, column=1, pady=10)

        # DROP DOWN GROUPS
        drop_down_frame = GUIInterface.CreateFrame(self.details_frame, border_width=0, fg_color='transparent')
        drop_down_frame.columnconfigure(0, weight=1)
        drop_down_frame.columnconfigure(1, weight=1)
        drop_down_frame.rowconfigure(0, weight=1)
        drop_down_frame.rowconfigure(1, weight=1)
        drop_down_frame.grid(row=9, column=1, sticky='nsew', pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        tz_frame, tz_label, tz_box = self.CreateDropdownField(values=pytz.all_timezones, entryname="Timezone")
        tz_box.set('Asia/Singapore')
        tz_frame.grid(row=0, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        calendars_frame, calendar_label, calendar_box = self.CreateDropdownField(values=[DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR], 
                                                                                entryname="Calendar")
        calendars_frame.grid(row=1, column=0, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        recur_option, recur_label, recur_box = self.CreateDropdownField(values=["None", "Daily", 'Weekly', 'Monthly'], 
                                                                        entryname="Repeated")
        recur_option.grid(row=1, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        recur_box.set(self.event.getRecurring())

        GUIInterface.current_frame = tmp_frame

    def UpdateEventWithDetails(self):
        details = self.getCurrentInputFieldsInfo()

        self.event.setName(details['Event'])
        self.event.setLocation(details['Location'])
        self.event.setDescription(details['Description'])
        print(self.event.description)

        self.event.set_S_Date(details['Start_Date'])
        self.event.set_E_Date(details['End_Date'])
        self.event.setStart_Time(details['Start_Time'])
        self.event.setEnd_Time(details['End_Time'])

    def UpdateInputFields(self):
        GUIInterface.UpdateEntry(self.details_entries["Event"], self.event.getName())
        GUIInterface.UpdateEntry(self.details_entries["Location"], self.event.getLocation())
        if self.event.getDescription() != '':
            GUIInterface.UpdateEntry(self.details_entries["Description"], self.event.getDescription())
        GUIInterface.UpdateEntry(self.details_entries["Start_Date"], self.event.get_S_Date())
        GUIInterface.UpdateEntry(self.details_entries["End_Date"], self.event.get_E_Date())
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], self.event.getStart_Time())
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], self.event.getEnd_Time())
    
    def Reset(self):
        GUIInterface.UpdateEntry(self.details_entries["Event"], "")
        GUIInterface.UpdateEntry(self.details_entries["Location"], "")
        GUIInterface.UpdateEntry(self.details_entries["Start_Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], "")
        GUIInterface.UpdateEntry(self.details_entries["Description"], "")
    
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
        return dropdown_frame, dropdown_label, dropdown_box
    
    def getCurrentInputFieldsInfo(self)->dict:
        details = {}
        for detail in self.details_entries:
            details[detail] = self.details_entries[detail].get()
        return details
    
    def PickDate(self, entry):
        date_window, cal, submit_btn = popup_mgr.CreateDateWindow()

        def GrabDate(entry, date:str, window):
            GUIInterface.UpdateEntry(entry, date)
            window.destroy()

        submit_btn.configure(command=lambda: GrabDate(entry, cal.get_date(), date_window))

    def ScheduleEvent(self):       
        self.UpdateEventWithDetails() # update event object before scheduling

        # Get input
        input = self.getCurrentInputFieldsInfo()

        # Handle missing or incorrect input for time fields
        if input['Event'] == '':
            messagebox.showerror(title=MISSING_INPUT_TITLE, message='Missing Event Name field!')
            return
        elif input['Start_Time'] == "":
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Missing Start Time field for {input["Event"]}')
            return
        elif input['End_Time'] == "":
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Missing End Time field for {input["Event"]}')
            return
        elif TextProcessingManager.CheckStringFormat(input['Start_Time']) == None:
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Incorrect Start Time provided for {input["Event"]} with {input["Start_Time"]}')
            return
        elif TextProcessingManager.CheckStringFormat(input['End_Time']) == None:
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Incorrect End Time provided for {input["Event"]} with {input["End_Time"]}')
            return
        
        # If no isses then create ics file
        # Process datetime to ics calendar format
        time_slots = []
        time_slots.append(input['Start_Time'])
        time_slots.append(input['End_Time'])

        ics_s_date = TextProcessingManager.ProcessDateToICSFormat(input['Start_Date'])
        ics_e_date = TextProcessingManager.ProcessDateToICSFormat(input['End_Date'])
        ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
        ics_s, ics_e = TextProcessingManager.ProcessICS(ics_s_date, ics_e_date, ics_time)

        input['Start_Time_ICS'] = ics_s
        input['End_Time_ICS'] = ics_e

        # Scheduling
        calendar = input['Calendar']
        if calendar == DEFAULT_CALENDAR: 
            EventsManager.ScheduleDefault(input, schedule_cb=self.ScheduleActions)
        elif calendar == GOOGLE_CALENDAR: 
            EventsManager.ScheduleGoogleCalendar(input, schedule_cb=self.ScheduleActions)
        elif calendar == OUTLOOK_CALENDAR: 
            EventsManager.ScheduleOutlookCalendar(input, schedule_cb=self.ScheduleActions)

    def ScheduleActions(self, id, platform=DEFAULT_CALENDAR):
        logging.info(f'SCHEDULE ACTIONS RAN FOR ID {id}')
        if platform != DEFAULT_CALENDAR:
            self.event.setPlatform(platform)
            self.event.setId(id)
            EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
        messagebox.showinfo(title=SUCCESS_TITLE, message='Successfully schedule event!')
        self.remove_cb(self.key)

    def getEvent(self):
        return self.event
    
    def ConvertEntryNameToKey(self, name:str):
        return name.replace(" ", "_")
    
    def Destroy(self):
        self.details_frame.destroy()