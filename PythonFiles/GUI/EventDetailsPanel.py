from GUI.GUIInterface import GUIInterface
from Managers.ErrorConfig import getParamValFromKwarg
from Events.EventsManager import Event
from Events.EventsManager import EventsManager
from Managers.TextProcessing import TextProcessingManager
import GUI.PopupManager as popup_mgr
import pytz
import Managers.MultiprocessingManager as multiprocess_mgr

# Calendar Intefaces
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
from Calendar.CalendarInterface import CalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
import Calendar.CalendarMacInterface as mac_calendar

from sys import platform
import os
import subprocess
import uuid

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
        remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(self.key), text='X', width=50)
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
        prio_frame, prio_label, prio_box = self.CreateDropdownField(values=priorities, entryname="Priority")
        prio_frame.grid(row=3, column=1, sticky='nsew',pady=self.gap)

        l_frame, l_entry = self.CreateEntryField(detail_entry_width, 
                                                 entryname="Location", 
                                                 placeholder_text='Location')
        l_frame.grid(row=4, column=1, sticky='nsew',pady=self.gap)

        s_d_frame, s_d_entry = self.CreateEntryField(detail_entry_width, 
                                                 entryname="Start Date", 
                                                 entry_state='disabled', 
                                                 placeholder_text='YYYY-MM-DD')
        s_d_frame.grid(row=5, column=1,sticky='nsew',pady=self.gap)
        s_d_entry.bind('<1>', lambda event, entry=s_d_entry: self.PickDate(entry))

        e_d_frame, e_d_entry = self.CreateEntryField(detail_entry_width, 
                                                 entryname="End Date", 
                                                 entry_state='disabled', 
                                                 placeholder_text='YYYY-MM-DD')
        e_d_frame.grid(row=6, column=1,sticky='nsew',pady=self.gap)
        e_d_entry.bind('<1>', lambda event, entry=e_d_entry: self.PickDate(entry))

        st_frame, st_entry = self.CreateEntryField(detail_entry_width, 
                                                   entryname="Start Time", 
                                                   placeholder_text="HH:MM:SS")
        st_frame.grid(row=7, column=1,sticky='nsew',pady=self.gap)

        et_frame, et_entry = self.CreateEntryField(detail_entry_width,
                                                   entryname="End Time", 
                                                   placeholder_text="HH:MM:SS")
        et_frame.grid(row=8, column=1,sticky='nsew',pady=self.gap)

        tz_frame, tz_label, tz_box = self.CreateDropdownField(values=pytz.all_timezones, entryname="Timezone")
        tz_frame.grid(row=9, column=1, sticky='nsew',pady=self.gap)
        tz_box.set('Asia/Singapore')

        calendars_frame, calendar_label, calendar_box = self.CreateDropdownField(values=["Default", "Google", 'Outlook'], entryname="Calendar")
        calendars_frame.grid(row=10, column=1, sticky='nsew',pady=self.gap)

        recur_option, recur_label, recur_box = self.CreateDropdownField(values=["None", "Daily", 'Weekly', 'Monthly'], entryname="Repeated")
        recur_option.grid(row=11, column=1, sticky='nsew',pady=self.gap)
        recur_box.set(self.event.getRecurring())

        schedule_btn = GUIInterface.CreateButton(on_click=self.ScheduleEvent, text='Schedule')
        schedule_btn.grid(row=12, column=1, sticky='nsew')

        GUIInterface.SetCurrentFrame(tmp_frame)

    def UpdateEventWithDetails(self):
        details = self.getCurrentInputFieldsInfo()
        self.event.setName(details['Event'])
        self.event.setLocation(details['Location'])
        self.event.set_S_Date(details['Start_Date'])
        self.event.set_E_Date(details['End_Date'])
        self.event.setStart_Time(details['Start_Time'])
        self.event.setEnd_Time(details['End_Time'])

    def UpdateInputFields(self):
        print(self.details_entries)
        GUIInterface.UpdateEntry(self.details_entries["Event"], self.event.getName())
        GUIInterface.UpdateEntry(self.details_entries["Location"], self.event.getLocation())
        GUIInterface.UpdateEntry(self.details_entries["Start_Date"], self.event.get_S_Date())
        GUIInterface.UpdateEntry(self.details_entries["End_Date"], self.event.get_E_Date())
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
        GUIInterface.UpdateEntry(self.details_entries["Start_Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Date"], "")
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
        #print("SCHEDULE CLICKED!")

        # Check if all required fields are filled
        if self.getEmptyInputFieldsCount() == self.rows:
            print("Required field is empty!")
            return
        
        input = self.getCurrentInputFieldsInfo()

        # Handle missing or incorrect input for time fields
        if input['Start_Time'] == "":
            print(f'Missing Start Time field for {input["Event"].upper()}[{input["Start_Date"]}]')
            return
        elif input['End_Time'] == "":
            print(f'Missing End Time field for {input["Event"].upper()}[{input["Start_Date"]}]')
            return
        elif TextProcessingManager.CheckStringFormat(input['Start_Time']) == None:
            print(f'Incorrect Start Time provided for {input["Event"].upper()}[{input["Start_Date"]}]')
            return
        elif TextProcessingManager.CheckStringFormat(input['End_Time']) == None:
            print(f'Incorrect End Time provided for {input["Event"].upper()}[{input["Start_Date"]}]')
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
        if calendar == 'Default':
            # No clash checking done for default yet
            # No need to add platform to event object as its default
            self.ScheduleDefault(input)
            #self.ScheduleActions(id=uuid.uuid4(), platform='Default')
        elif calendar == 'Google': self.ScheduleGoogleCalendar(input)
        elif calendar == 'Outlook': self.ScheduleOutlookCalendar(input)

    def ScheduleActions(self, id, platform='Default'):
        self.event.setPlatform(platform)
        self.event.setId(id)
        EventsManager.AddEventToEventDB(self.event, EventsManager.events_db)
        EventsManager.WriteEventDBToJSON()
        self.remove_cb(self.key)

    # Right now can only handle 1 event only 
    def ScheduleDefault(self, event):
        # Mac
        if platform == 'darwin':
            filename = self.CreateICSFileFromInput(event)
            if filename == None:
                print('FAILED TO CREATE ICS FILE FOR MAC')
                return
            file = CalendarInterface.getICSFilePath(filename)
            def schedule_mac(): 
                print('ran')
                subprocess.run(['open', file])
                self.ScheduleActions(id=uuid.uuid4(), platform='Default')
            popup_mgr.PopupWithBtn(subtitle_1='Warning',
                                   subtitle_2='No checks for other events are done for this.\nAre you sure you want to schedule?',
                                   button_cb=schedule_mac)
        # Windows
        else:
            filename = self.CreateICSFileFromInput(event)
            if filename == None:
                print('FAILED TO CREATE ICS FILE FOR WINDOWS')
                return
            file = CalendarInterface.getICSFilePath(filename)
            os.startfile(file)

    def ScheduleGoogleCalendar(self, event)->[str, list]:
        filename = self.CreateICSFileFromInput(event)
        if filename == None:
            print('FAILED TO CREATE ICS FILE FOR GOOGLE')
            return ''
        google_event = GoogleCalendarInterface.Parse_ICS(filename)

        # Check for existing events
        existing_events = GoogleCalendarInterface.getEvents(time_min=google_event.getStartDate(), 
                                                            time_max=google_event.getUNTILDate())
        overlapped_events = []
        if len(existing_events) > 0: overlapped_events = GoogleCalendarInterface.EventOverlaps(google_event, existing_events)

        # Method to scheudle google event
        def schedule_google_calendar_event(): 
            id = GoogleCalendarInterface.ScheduleCalendarEvent(googleEvent=google_event)
            if id == '': popup_mgr.FailedPopup('Failed to schedule event for reasons')
            else: self.ScheduleActions(id=id, platform='Google')

        # Handle clash of events
        if len(overlapped_events) > 0:
            names = [x.getEvent() for x in overlapped_events]
            base_text = ''
            for t in names: base_text += (t + ', ')
            popup_mgr.PopupWithBtn(subtitle_1='Are you sure you want to schedule this event?',
                                   subtitle_2='It clashes with the following events:',
                                   textbox_content=base_text, 
                                   button_cb=schedule_google_calendar_event)
        else: schedule_google_calendar_event()

    def ScheduleOutlookCalendar(self, event)->str:
        filename = self.CreateICSFileFromInput(event)
        if filename == None:
            print('FAILED TO CREATE ICS FILE FOR OUTLOOK')
            return ''
        outlook_event = outlook_interface.parse_ics(filename).event
        # Check for any pre-existing event
        filter_param = {
        '$filter': f"start/dateTime ge {outlook_event['start']['dateTime']} and end/dateTime le {outlook_event['end']['dateTime']}"
        }
        cal_events ={}
        try: cal_events = outlook_interface.send_flask_req('get_events', param_data=filter_param)[1]['value']
        except:
            if 'OUTLOOK' in multiprocess_mgr.mgr_processes: multiprocess_mgr.terminate_process('OUTLOOK')
        
        # Response format
        #(True, {'@odata.context': "", 'value': []})
        if cal_events == {}: 
            popup_mgr.FailedPopup('Failed to schedule event for [OUTLOOK] due to failed authentication')
            return ''

        def schedule_outlook_calendar_event():
            response = outlook_interface.send_flask_req(req='create_event', 
                                                        json_data={'event': outlook_event})
            details = response[1]
            if 'id' not in details: popup_mgr.FailedPopup('Failed to schedule event for reasons')
            else: self.ScheduleActions(id=details['id'], platform='Outlook')

        # Cannot pass an entire dictionary as a param 
        if len(cal_events) > 0:
            names = [x['subject'] for x in cal_events]
            base_text = ''
            for t in names: base_text += (t + ', ')
            popup_mgr.PopupWithBtn(subtitle_1='Are you sure you want to schedule this event?',
                                   subtitle_2='It clashes with the following events:',
                                   textbox_content=base_text, 
                                   button_cb=schedule_outlook_calendar_event)
        else: schedule_outlook_calendar_event()

    # Creates ICS files to be parsed 
    # 1 ICS = should have 1 VEVENT
    # returns names of file created
    def CreateICSFileFromInput(self, event)->str:
        desp = event["Description"]
        priority = int(event["Priority"])
        location = event["Location"]
        tz = event['Timezone']
        title = event["Event"]
        ics_s = event["Start_Time_ICS"]
        ics_e = event["End_Time_ICS"]

        ics_s = ics_s.replace(tzinfo=pytz.timezone(tz))
        ics_e = ics_e.replace(tzinfo=pytz.timezone(tz))

        time_difference =  ics_e - ics_s
        hours, remainder = divmod(time_difference.seconds, 3600)

        rrule = {'freq': event["Repeated"].lower(),
                 'until': ics_e,
                } if event['Repeated'] != 'None' else {}
        
        # Create ICS File
        file_name = CalendarInterface.CreateICSEvent(e_name=title,
                                                    e_description=desp,
                                                    s_datetime=ics_s,
                                                    e_datetime=ics_e,
                                                    e_location=location,
                                                    e_priority=int(priority),
                                                    rrule=rrule,
                                                    duration=hours)
        
        #file_name = f'{title}_{ics_s}'
        #CalendarInterface.WriteToFile(file_name)
        return file_name