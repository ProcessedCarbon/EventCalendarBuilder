from tkinter import messagebox
import pytz
import logging
from customtkinter import *

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import MISSING_INPUT_TITLE, EVENT_DETAILS_PANEL_ROWS, SUCCESS_TITLE, EVENT_DETAILS_PANEL_DETAIL_GAP, EVENT_ROW_GAP, EVENT_DETAILS_PANEL_ENTRY_WIDTH_MODIFIER, MISSING_EVENT_NAME_INPUT_MSG, SCHEDULE_SUCCESS_MSG, INVALID_INPUT_TITLE, ALERT_OPTIONS, RECURRING_OPTIONS, MAX_EVENT_TITLE, MAX_EVENT_REACHED_MESSAGE
from Events.Event import Event
from Events.EventsManager import EventsManager
from Events.Event_Constants import EVENT_LIMIT
from Managers.TextProcessing import TextProcessingManager
from Calendar.CalendarConstants import DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR
import GUI.PopupManager as popup_mgr
from Calendar.CalendarInterface import CalendarInterface
from Managers.DateTimeManager import DateTimeManager

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
                                padx=EVENT_ROW_GAP, 
                                pady=EVENT_ROW_GAP,
                                ipadx=EVENT_ROW_GAP)
        
        # Rows
        for i in range(EVENT_DETAILS_PANEL_ROWS):
            self.details_frame.rowconfigure(i, weight=1)
        
        # Columns
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.columnconfigure(1, weight=10)
        self.details_frame.columnconfigure(2, weight=1)

        self.details_frame.update() # needs to be grid and updated before other GUI as following UI needs the updated frame params

        # Event Title
        self.event_title = GUIInterface.CreateLabel(text=f"Event {self.row}", font=GUIInterface.getCTKFont(size=20, weight="bold"))

        # GUI Attributes
        detail_entry_width = self.details_frame.winfo_width() * EVENT_DETAILS_PANEL_ENTRY_WIDTH_MODIFIER

        # Buttons
        remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(self.key), text='X', width=50)
        dup_btn = GUIInterface.CreateButton(on_click=lambda:self.dup_cb(self.event.getId()), text='+', width=40)
        schedule_btn = GUIInterface.CreateButton(on_click=self.ScheduleEvent, text='Schedule this event')

        # Input
        e_frame, e_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Event", 
                                                placeholder_text='Title')

        desp_frame, desp_entry = self.CreateTextboxField(detail_entry_width, 
                                                        entryname="Description")

        l_frame, l_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Location", 
                                                placeholder_text='Location')

        s_d_frame, s_d_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Start Date", 
                                                entry_state='disabled', 
                                                placeholder_text='YYYY-MM-DD')

        e_d_frame, e_d_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="End Date", 
                                                entry_state='disabled', 
                                                placeholder_text='YYYY-MM-DD')

        st_frame, st_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Start Time", 
                                                placeholder_text="HH:MM:SS")

        et_frame, et_entry = self.CreateEntryField(detail_entry_width,
                                                entryname="End Time", 
                                                placeholder_text="HH:MM:SS")
        
        # DROP DOWN GROUPS
        drop_down_frame = GUIInterface.CreateFrame(self.details_frame, border_width=0, fg_color='transparent')
        drop_down_frame.columnconfigure(0, weight=1)
        drop_down_frame.columnconfigure(1, weight=1)
        drop_down_frame.rowconfigure(0, weight=1)
        drop_down_frame.rowconfigure(1, weight=1)

        self.tz_frame, self.tz_label, self.tz_box = self.CreateDropdownField(values=pytz.all_timezones, entryname="Timezone")
        self.tz_box.set('Asia/Singapore')

        self.calendars_frame, self.calendar_label, self.calendar_box = self.CreateDropdownField(values=[DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR], entryname="Calendar")

        self.recur_frame, self.recur_label, self.recur_box = self.CreateDropdownField(values=RECURRING_OPTIONS, entryname="Repeated")
        self.recur_box.set(self.event.getRecurring())

        # Alert Options
        self.alert_frame, self.alert_label, self.alert_box = self.CreateDropdownField(values=ALERT_OPTIONS, entryname="Alert")
        self.alert_label.configure(text=f"{self.alert_label.cget('text').split(':')[0]} (minutes):")
        self.alert_box.set(ALERT_OPTIONS[1])

        # Bindings
        s_d_entry.bind('<1>', lambda event, entry=s_d_entry: self.PickDate(entry))
        e_d_entry.bind('<1>', lambda event, entry=e_d_entry: self.PickDate(entry))

        # Grid GUI
        self.event_title.grid(row=0, column=1, pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        dup_btn.grid(row=0, column=2, pady=EVENT_DETAILS_PANEL_DETAIL_GAP, sticky='e')
        remove_btn.grid(row=0, column=3, pady=EVENT_DETAILS_PANEL_DETAIL_GAP, sticky='e', padx=(0, EVENT_DETAILS_PANEL_DETAIL_GAP))

        e_frame.grid(row=1, column=1,sticky='nsew', pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        desp_frame.grid(row=2, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        l_frame.grid(row=3, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        s_d_frame.grid(row=4, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        e_d_frame.grid(row=5, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        st_frame.grid(row=6, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        et_frame.grid(row=7, column=1,sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        drop_down_frame.grid(row=9, column=1, sticky='nsew', pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        schedule_btn.grid(row=10, column=1, pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        # Under drop down frame
        self.tz_frame.grid(row=0, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        self.calendars_frame.grid(row=1, column=0, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        self.recur_frame.grid(row=1, column=1, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)
        self.alert_frame.grid(row=0, column=0, sticky='nsew',pady=EVENT_DETAILS_PANEL_DETAIL_GAP)

        GUIInterface.current_frame = tmp_frame

    def UpdateEventWithDetails(self):
        details = self.getCurrentInputFieldsInfo()

        self.event.setName(details['Event'])
        self.event.setLocation(details['Location'])
        self.event.setDescription(details['Description'])

        self.event.set_S_Date(details['Start_Date'])
        self.event.set_E_Date(details['End_Date'])
        self.event.setStart_Time(details['Start_Time'])
        self.event.setEnd_Time(details['End_Time'])

        self.event.setTimezone(tz=self.tz_box.get())
        self.event.setRecurring(recur=self.recur_box.get())
        self.event.setAlert(minutes=int(self.alert_box.get()))

    def UpdateInputFields(self):
        GUIInterface.UpdateEntry(self.details_entries["Event"], self.event.getName())
        GUIInterface.UpdateEntry(self.details_entries["Location"], self.event.getLocation())
        if self.event.getDescription() != '':
            GUIInterface.UpdateTextBox(self.details_entries["Description"], "normal", self.event.getDescription())
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
        GUIInterface.UpdateTextBox(self.details_entries["Description"], "normal" ,"")
    
    # Create GUI
    def CreateEntryField(self, width:int, entryname:str, entry_state='normal', placeholder_text=None):
        key = self.ConvertEntryNameToKey(entryname)
        e_frame, e_label, e_entry = GUIInterface.CreateEntryWithLabel(label= entryname + ":",
                                                                    entry_width=width, 
                                                                    entry_state=entry_state,
                                                                    placeholder_text=placeholder_text)
        self.details_entries[key] = e_entry
        return e_frame, e_entry
    
    def CreateTextboxField(self, width:int, entryname:str, textbox_state='normal'):
        key = self.ConvertEntryNameToKey(entryname)
        e_frame, e_label, e_textbox = GUIInterface.CreateTextboxWithLabel(label= entryname + ":",
                                                                        textbox_width=width, 
                                                                        textbox_state=textbox_state)
        self.details_entries[key] = e_textbox
        return e_frame, e_textbox

    def CreateDropdownField(self, values:list[str], entryname:str):
        key = self.ConvertEntryNameToKey(entryname)
        dropdown_frame, dropdown_label, dropdown_box = GUIInterface.CreateOptionMenuWithLabel(label=entryname +":", dropdown=values)
        self.details_entries[key] = dropdown_box
        return dropdown_frame, dropdown_label, dropdown_box
    
    def getCurrentInputFieldsInfo(self)->dict:
        details = {}
        for detail in self.details_entries:
            if detail == 'Description':
                details[detail] = GUIInterface.RetrieveCurrentInputFromTextbox(self.details_entries[detail])
            else:
                details[detail] = self.details_entries[detail].get()
        return details
    
    def PickDate(self, entry):
        date_window, cal, submit_btn = popup_mgr.CreateDateWindow()

        def GrabDate(entry, date:str, window):
            GUIInterface.UpdateEntry(entry, date)
            window.destroy()

        submit_btn.configure(command=lambda: GrabDate(entry, cal.get_date(), date_window))

    def ScheduleEvent(self):     
        # Handle event limit reached
        if len(EventsManager.events_db) >= EVENT_LIMIT:
            messagebox.showinfo(title=MAX_EVENT_TITLE, message=MAX_EVENT_REACHED_MESSAGE)
            return
        
        self.UpdateEventWithDetails() # update event object before scheduling

        # Get input
        input = self.getCurrentInputFieldsInfo()

        # Handle missing or incorrect input for time fields
        if self.CheckInputs(input) == False:
            return
        
        # If no isses then create ics file
        # Process datetime to ics calendar format
        CalendarInterface.AppendStartTime(input=input)

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
            EventsManager.AddEventToEventDB(self.event, EventsManager.events_db, store_object=False)
        messagebox.showinfo(title=SUCCESS_TITLE, message=SCHEDULE_SUCCESS_MSG)
        self.remove_cb(self.key)

    def getEvent(self):
        return self.event
    
    def ConvertEntryNameToKey(self, name:str):
        return name.replace(" ", "_")
    
    def Destroy(self):
        self.details_frame.destroy()
    
    def CheckInputs(self, input):
        # Handle missing or incorrect input for time fields
        if input['Event'] == '':
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=MISSING_EVENT_NAME_INPUT_MSG)
            return False
        elif input['Start_Time'] == "":
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Missing Start Time field for {input["Event"]}')
            return False
        elif input['End_Time'] == "":
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Missing End Time field for {input["Event"]}')
            return False
        elif TextProcessingManager.CheckStringFormat(input['Start_Time']) == None:
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Incorrect Start Time provided for {input["Event"]} with {input["Start_Time"]}')
            return False
        elif TextProcessingManager.CheckStringFormat(input['End_Time']) == None:
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Incorrect End Time provided for {input["Event"]} with {input["End_Time"]}')
            return False
        elif TextProcessingManager.CheckStringFormat(input['Start_Date'], regex="^\d{4}-\d{2}-\d{2}$") == None:
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Incorrect Start Date provided for {input["Event"]} with {input["Start_Date"]}')
            return False
        elif TextProcessingManager.CheckStringFormat(input['End_Date'], regex="^\d{4}-\d{2}-\d{2}$") == None:
            messagebox.showerror(title=MISSING_INPUT_TITLE, message=f'Incorrect End Date provided for {input["Event"]} with {input["End_Date"]}')
            return False
        elif DateTimeManager.CompareDates(date1=input['End_Date'], date2=input['Start_Date']) == False:
            messagebox.showerror(title=INVALID_INPUT_TITLE, message=f'Invalid Dates provided\nStart Date: {input["Start_Date"]}\nEnd Date: {input["End_Date"]}')
            return False
        return True