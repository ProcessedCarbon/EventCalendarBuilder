from GUI.GUIInterface import GUIInterface
from Events.EventsManager import Event
from Events.EventsManager import EventsManager
from Managers.TextProcessing import TextProcessingManager
from Calendar.CalendarConstants import DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR
import GUI.PopupManager as popup_mgr
from tkinter import messagebox
import pytz
import logging

class EventDetailsPanel:
    outlook_supported_tzs = None
    def __init__(self, parent, event:Event, remove_cb, key:int, gap:int=10, **grid_params):
        self.gap = gap
        self.parent = parent
        self.grid_params = grid_params

        self.details_entries = {}
        self.filled = False
        self.details_frame = None
        self.event = event
        self.rows = 12
        self.key = key
        self.remove_cb = remove_cb

        self.GUI()
        
    def GUI(self):
        tmp_frame = GUIInterface.current_frame
        self.details_frame = GUIInterface.CreateFrame(self.parent, 
                                                    fg_color=GUIInterface.color_palette['CTkFrame']['border_color'][0])

        # Find grid in parent to place this event panel
        row = GUIInterface.getParamValFromKwarg("row", self.grid_params, default=0)
        column = GUIInterface.getParamValFromKwarg("column", self.grid_params, default=0)
        sticky = GUIInterface.getParamValFromKwarg("sticky", self.grid_params, default='nsew')
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
        remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(self.key), text='X', width=50)
        remove_btn.grid(row=0, column=1, pady=10, sticky='e')

        e_frame, e_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Event", 
                                                placeholder_text='Title')
        e_frame.grid(row=1, column=1,sticky='nsew', pady=self.gap)

        desp_frame, desp_entry = self.CreateEntryField(detail_entry_width, 
                                                    entryname="Description", 
                                                    placeholder_text='Description')
        desp_frame.grid(row=2, column=1, sticky='nsew',pady=self.gap)

        l_frame, l_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Location", 
                                                placeholder_text='Location')
        l_frame.grid(row=3, column=1, sticky='nsew',pady=self.gap)

        s_d_frame, s_d_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Start Date", 
                                                entry_state='disabled', 
                                                placeholder_text='YYYY-MM-DD')
        s_d_entry.bind('<1>', lambda event, entry=s_d_entry: self.PickDate(entry))
        s_d_frame.grid(row=4, column=1,sticky='nsew',pady=self.gap)

        e_d_frame, e_d_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="End Date", 
                                                entry_state='disabled', 
                                                placeholder_text='YYYY-MM-DD')
        e_d_entry.bind('<1>', lambda event, entry=e_d_entry: self.PickDate(entry))
        e_d_frame.grid(row=5, column=1,sticky='nsew',pady=self.gap)

        st_frame, st_entry = self.CreateEntryField(detail_entry_width, 
                                                entryname="Start Time", 
                                                placeholder_text="HH:MM:SS")
        st_frame.grid(row=6, column=1,sticky='nsew',pady=self.gap)

        et_frame, et_entry = self.CreateEntryField(detail_entry_width,
                                                entryname="End Time", 
                                                placeholder_text="HH:MM:SS")
        et_frame.grid(row=7, column=1,sticky='nsew',pady=self.gap)
        
        schedule_btn = GUIInterface.CreateButton(on_click=self.ScheduleEvent, text='Schedule')
        schedule_btn.grid(row=10, column=1, pady=10)

        # DROP DOWN GROUPS
        drop_down_frame = GUIInterface.CreateFrame(self.details_frame, border_width=0, fg_color='transparent')
        drop_down_frame.columnconfigure(0, weight=1)
        drop_down_frame.columnconfigure(1, weight=1)
        drop_down_frame.rowconfigure(0, weight=1)
        drop_down_frame.rowconfigure(1, weight=1)
        drop_down_frame.grid(row=9, column=1, sticky='nsew', pady=self.gap)

        tz_frame, tz_label, tz_box = self.CreateDropdownField(values=pytz.all_timezones, entryname="Timezone")
        tz_box.set('Asia/Singapore')
        tz_frame.grid(row=0, column=1, sticky='nsew',pady=self.gap)

        calendars_frame, calendar_label, calendar_box = self.CreateDropdownField(values=[DEFAULT_CALENDAR, GOOGLE_CALENDAR, OUTLOOK_CALENDAR], 
                                                                                entryname="Calendar")
        calendars_frame.grid(row=1, column=0, sticky='nsew',pady=self.gap)

        recur_option, recur_label, recur_box = self.CreateDropdownField(values=["None", "Daily", 'Weekly', 'Monthly'], 
                                                                        entryname="Repeated")
        recur_option.grid(row=1, column=1, sticky='nsew',pady=self.gap)
        recur_box.set(self.event.getRecurring())

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

    def UpdateInputFields(self):
        #print(self.details_entries)
        GUIInterface.UpdateEntry(self.details_entries["Event"], self.event.getName())
        GUIInterface.UpdateEntry(self.details_entries["Location"], self.event.getLocation())
        GUIInterface.UpdateEntry(self.details_entries["Start_Date"], self.event.get_S_Date())
        GUIInterface.UpdateEntry(self.details_entries["End_Date"], self.event.get_E_Date())
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], self.event.getStart_Time())
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], self.event.getEnd_Time())
        self.filled = True
    
    def Reset(self):
        self.filled = False

        GUIInterface.UpdateEntry(self.details_entries["Event"], "")
        GUIInterface.UpdateEntry(self.details_entries["Location"], "")
        GUIInterface.UpdateEntry(self.details_entries["Start_Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], "")
        GUIInterface.UpdateEntry(self.details_entries["Description"], "")

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
        return dropdown_frame, dropdown_label, dropdown_box
    
    def ConvertEntryNameToKey(self, name:str):
        return name.replace(" ", "_")
    
    def getCurrentInputFieldsInfo(self)->dict:
        details = {}
        for detail in self.details_entries:
            details[detail] = self.details_entries[detail].get()
        return details
    
    def getEvent(self):
        return self.event
    
    def PickDate(self, entry):
        date_window, cal, submit_btn = popup_mgr.CreateDateWindow()
        submit_btn.configure(command=lambda:self.GrabDate(entry, cal.get_date(), date_window))

    def GrabDate(self, entry, date:str, window):
        GUIInterface.UpdateEntry(entry, date)
        window.destroy()

    def ScheduleEvent(self):       
        # update event object before scheduling
        self.UpdateEventWithDetails()

        # Get input
        input = self.getCurrentInputFieldsInfo()

        # Handle missing or incorrect input for time fields
        if input['Event'] == '':
            messagebox.showerror(title='Missing input', message='Missing Event Name field!')
            return
        elif input['Start_Time'] == "":
            messagebox.showerror(title='Missing input', message=f'Missing Start Time field for {input["Event"].upper()}[{input["Start_Date"]}]')
            return
        elif input['End_Time'] == "":
            messagebox.showerror(title='Missing input', message=f'Missing End Time field for {input["Event"].upper()}[{input["Start_Date"]}]')
            return
        elif TextProcessingManager.CheckStringFormat(input['Start_Time']) == None:
            messagebox.showerror(title='Missing input', message=f'Incorrect Start Time provided for {input["Event"].upper()}[{input["Start_Date"]}]')
            return
        elif TextProcessingManager.CheckStringFormat(input['End_Time']) == None:
            messagebox.showerror(title='Missing input', message=f'Incorrect End Time provided for {input["Event"].upper()}[{input["Start_Date"]}]')
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
        if calendar == DEFAULT_CALENDAR: EventsManager.ScheduleDefault(input, schedule_cb=self.ScheduleActions)
        elif calendar == GOOGLE_CALENDAR: EventsManager.ScheduleGoogleCalendar(input, schedule_cb=self.ScheduleActions)
        elif calendar == OUTLOOK_CALENDAR: EventsManager.ScheduleOutlookCalendar(input, schedule_cb=self.ScheduleActions)

    def ScheduleActions(self, id, platform=DEFAULT_CALENDAR):
        logging.info(f'SCHEDULE ACTIONS RAN FOR ID {id}')
        if platform != DEFAULT_CALENDAR:
            self.event.setPlatform(platform)
            self.event.setId(id)
            EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
        messagebox.showinfo(title='Success', message='Successfully schedule event!')
        self.remove_cb(self.key)