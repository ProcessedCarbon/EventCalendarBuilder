from tkinter import messagebox
from sys import platform
import logging
import pytz

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import SUCCESS_TITLE, EVENT_ROW_GAP, EVENT_DETAILS_PANEL_CARD_GAP, EVENT_DETAILS_CARD_ENTRY_WIDTH_MODIFIER, FAILED_TITLE, WARNING_TITLE, INVALID_INPUT_TITLE, MISSING_INPUT_TITLE, MISSING_EVENT_NAME_INPUT_MSG, NO_GOOGLE_CONNECTION_MSG, NO_OUTLOOK_CONNECTION_MSG, FAILED_ICS_PARSING, ASK_REMOVE_EVENT_MSG, ALERT_OPTIONS, RECURRING_OPTIONS
from Events.EventsManager import EventsManager
import Calendar.CalendarMacInterface as cal_mac
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
from Calendar.CalendarConstants import DEFAULT_CALENDAR, OUTLOOK_CALENDAR, GOOGLE_CALENDAR
from Calendar.CalendarInterface import CalendarInterface
from Managers.DateTimeManager import DateTimeManager
from Managers.TextProcessing import TextProcessingManager
import GUI.PopupManager as popup_mgr

class EventCard:
    def __init__(self, parent, row, event_details:dict, remove_cb, index:int) -> None:

        # Variables
        tmp_frame = GUIInterface.current_frame
        self.event_details = event_details
        self.index = index
        self.remove_cb = remove_cb
        self.editable = False
        frame_color = GUIInterface.color_palette['CTkFrame']['border_color'][0]

        self.card_frame = GUIInterface.CreateFrame(parent, 
                                                fg_color=frame_color)
        self.card_frame.grid(row=row, 
                            column=0, 
                            sticky='nsew', 
                            padx=EVENT_ROW_GAP, 
                            pady=EVENT_ROW_GAP,)
        GUIInterface.CreateGrid(self.card_frame, rows=[1] * len(event_details), cols=[1])
        self.card_frame.update() # needs to be grid and updated before other GUI as following UI needs the updated frame params

        # Details Attributes
        attribute_width= self.card_frame.winfo_width() * EVENT_DETAILS_CARD_ENTRY_WIDTH_MODIFIER

        # Details
        self.platform_label = GUIInterface.CreateLabel(text=f"Platform: {self.event_details['platform']}", font = GUIInterface.getCTKFont(size=15, weight="bold"))

        # title
        self.n_frame,  self.n_label, self.n_entry = GUIInterface.CreateEntryWithLabel(label= "Name:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')

        # desc
        self.desc_frame, self.desc_label, self.desc_textbox = GUIInterface.CreateTextboxWithLabel(label= "Description:",
                                                                                                textbox_width=attribute_width, 
                                                                                                textbox_state='disabled')
        # location
        self.l_frame, self.l_label, self.l_entry = GUIInterface.CreateEntryWithLabel(label= "Location:",
                                                                                    entry_width=attribute_width, 
                                                                                    entry_state='disabled')
        # start date
        self.s_d_frame, self.s_d_label, self.s_d_entry = GUIInterface.CreateEntryWithLabel(label= "Start Date:",
                                                                                            entry_width=attribute_width, 
                                                                                            entry_state='disabled')
        # end date
        self.e_d_frame, self.e_d_label, self.e_d_entry = GUIInterface.CreateEntryWithLabel(label= "End Date:",
                                                                                            entry_width=attribute_width, 
                                                                                            entry_state='disabled')
        # start time
        self.st_frame, self.st_label, self.st_entry = GUIInterface.CreateEntryWithLabel(label= "Start Time:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')
        # end time
        self.et_frame, self.et_label, self.et_entry = GUIInterface.CreateEntryWithLabel(label= "End Time:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')
        
        # Dropsdowns
        tmp = GUIInterface.current_frame
        self.drop_down_frame = GUIInterface.CreateFrame(GUIInterface.current_frame, border_color=frame_color, fg_color=frame_color)
        GUIInterface.CreateGrid(self.drop_down_frame, rows=[1], cols=[1, 1, 1])

        self.tz_frame, self.tz_label, self.tz_box = GUIInterface.CreateOptionMenuWithLabel(label="Timezone:", dropdown=pytz.all_timezones)
        self.tz_box.configure(state='disabled')
        self.tz_label.grid(row=0, column=0, sticky='e')

        self.recur_frame, self.recur_label, self.recur_box = GUIInterface.CreateOptionMenuWithLabel(label="Repeated:", dropdown=RECURRING_OPTIONS)
        self.recur_box.configure(state='disabled')
        self.recur_label.grid(row=0, column=0, sticky='e')

        self.alert_frame, self.alert_label, self.alert_box = GUIInterface.CreateOptionMenuWithLabel(label="Alert (minutes):", dropdown=ALERT_OPTIONS)
        self.alert_box.configure(state='disabled')
        self.alert_label.grid(row=0, column=0, sticky='e')

        GUIInterface.current_frame = tmp

        # Buttons
        tmp = GUIInterface.current_frame
        self.button_frame = GUIInterface.CreateFrame(GUIInterface.current_frame, 
                                                                fg_color=frame_color,
                                                                border_color=frame_color) 
        GUIInterface.CreateGrid(self.button_frame, rows=[1], cols=[1, 1, 1])

        self.remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(index), 
                                                    text='Remove this event')
        
        self.edit_btn = GUIInterface.CreateButton(on_click=self.OnEditClick, 
                                                    text='Edit this event')
        
        self.update_btn = GUIInterface.CreateButton(on_click=self.UpdateOnCalendar, 
                                                    text='Update this event')
        GUIInterface.current_frame = tmp

        # Update entries
        self.UpdateEntries()

        # Grid GUI
        self.platform_label.grid(row=1, column=0, sticky='ew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.n_frame.grid(row=2, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.desc_frame.grid(row=3, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.l_frame.grid(row=4, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.s_d_frame.grid(row=5, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.e_d_frame.grid(row=6, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.st_frame.grid(row=7, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.et_frame.grid(row=8, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)

        # Dropdown
        self.drop_down_frame.grid(row=9, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.tz_frame.grid(row=0, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.recur_frame.grid(row=0, column=1, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.alert_frame.grid(row=0, column=2, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)

        # Buttons
        self.button_frame.grid(row=0, column=0,  sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.remove_btn.grid(row=1, column=0)
        self.edit_btn.grid(row=1, column=1)
        self.update_btn.grid(row=1, column=2)

        GUIInterface.current_frame = tmp_frame

    def Destroy(self, askBeforeDelete = True)->bool:
        removed_from_cal = self.RemoveFromCalender(askCheck=askBeforeDelete)
        if removed_from_cal:
            success = EventsManager.RemoveFromEventDB(self.event_details['id'], EventsManager.events_db)
            if success:
                self.card_frame.destroy()
                return True
        return False

    def UpdateEntries(self):
        GUIInterface.UpdateEntry(self.n_entry, self.event_details['name'])
        GUIInterface.UpdateTextBox(self.desc_textbox, "disabled", self.event_details['description'])
        GUIInterface.UpdateEntry(self.l_entry, self.event_details['location'])
        GUIInterface.UpdateEntry(self.s_d_entry, self.event_details['s_date'])
        GUIInterface.UpdateEntry(self.e_d_entry, self.event_details['e_date'])
        GUIInterface.UpdateEntry(self.st_entry, self.event_details['start_time'])
        GUIInterface.UpdateEntry(self.et_entry, self.event_details['end_time'])

        self.tz_box.set(self.event_details['timezone'])
        self.recur_box.set(self.event_details['recurring'])
        self.alert_box.set(self.event_details['alert']) 
    
    def UpdateEventDetails(self):
        self.event_details['name'] = self.n_entry.get()
        self.event_details['description'] = GUIInterface.RetrieveCurrentInputFromTextbox(self.desc_textbox)
        self.event_details['location'] = self.l_entry.get()
        self.event_details['s_date'] = self.s_d_entry.get()
        self.event_details['e_date'] = self.e_d_entry.get()
        self.event_details['start_time'] = self.st_entry.get()
        self.event_details['end_time'] = self.et_entry.get()
        self.event_details['timezone'] = self.tz_box.get()
        self.event_details['recurring'] = self.recur_box.get()
        self.event_details['alert'] = self.alert_box.get()

    def ChangeEntryState(self, state):
        self.n_entry.configure(state=state)
        self.desc_textbox.configure(state=state)
        self.l_entry.configure(state=state)
        self.st_entry.configure(state=state)
        self.et_entry.configure(state=state)
        self.tz_box.configure(state=state)
        self.recur_box.configure(state=state)
        self.alert_box.configure(state=state)

        # Bindings
        if state == 'normal':
            self.s_d_entry.bind('<1>', lambda event, entry=self.s_d_entry: self.PickDate(entry))
            self.e_d_entry.bind('<1>', lambda event, entry=self.e_d_entry: self.PickDate(entry))
        else:
            self.s_d_entry.unbind('<1>')
            self.e_d_entry.unbind('<1>')
        
    def OnEditClick(self):
        self.editable = not self.editable
        state = self.editable == False and 'disabled'  or 'normal'
        self.ChangeEntryState(state=state)

    def RemoveFromCalender(self, askCheck = True)->bool:
        try:
            res = messagebox.askokcancel(title=WARNING_TITLE, message=ASK_REMOVE_EVENT_MSG) if askCheck else not askCheck

            if res:
                if self.event_details['platform'] == DEFAULT_CALENDAR: # Should not occur as Default calendar methods are not saved locally
                    if platform == 'darwin': 
                        cal_mac.RemoveMacCalendarEvents(self.event_details['name'])
                    else: 
                        removed = None
                        response = None
                        removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.event_details['id']})
                        if removed == False and response == None:
                            messagebox.showerror(title=FAILED_TITLE, message=NO_OUTLOOK_CONNECTION_MSG)
                            return False
                
                elif self.event_details['platform'] == GOOGLE_CALENDAR:
                    removed, reason = GoogleCalendarInterface.DeleteEvent(self.event_details['id'])
                    if removed == False and reason == '':
                        messagebox.showerror(title=FAILED_TITLE, message=NO_GOOGLE_CONNECTION_MSG)
                        return False
                
                elif self.event_details['platform'] == OUTLOOK_CALENDAR:
                    removed = None
                    response = None
                    try:
                        removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.event_details['id']})
                    except:
                        pass
                    if removed == False and response == None:
                        messagebox.showerror(title=FAILED_TITLE, message=NO_OUTLOOK_CONNECTION_MSG)
                        return False

                messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully removed {self.event_details["name"]} from {self.event_details["platform"]} Calendar')
                return True
            return False            
        except:
            messagebox.showinfo(title=FAILED_TITLE, message=f'Failed removal of {self.event_details["name"]}')
            return False
        
    def UpdateOnCalendar(self):
        try:
            self.UpdateEventDetails()
            
            if self.editable == True:
                self.editable = False
                self.ChangeEntryState(state='disabled')

            input = {
                'Event': self.event_details['name'],
                'Description': self.event_details['description'],
                'Location': self.event_details['location'],
                'Start_Date': self.event_details['s_date'],
                'End_Date': self.event_details['e_date'],
                'Start_Time': self.event_details['start_time'],
                'End_Time': self.event_details['end_time'],
                'Timezone': self.event_details['timezone'],
                'Repeated': self.event_details['recurring'],
                'Platform': self.event_details['platform'],
                'Alert': self.event_details['alert'],
            }

            # Handle missing or incorrect input for time fields
            if self.CheckInputs(input) == False:
                return

            # If no isses then create ics file
            # Process datetime to ics calendar format
            CalendarInterface.AppendStartTime(input=input)
                
            if self.event_details['platform'] == DEFAULT_CALENDAR: # Should not occur as Default calendar methods are not saved locally
                messagebox.showinfo(title=WARNING_TITLE, message=f'Update of event not supported for {DEFAULT_CALENDAR} Calendar events')
            
            elif self.event_details['platform'] == GOOGLE_CALENDAR:
                # Create google event
                filename = EventsManager.CreateICSFileFromInput(input)
                if filename == None:
                    logging.error(f'[{__name__}] FAILED TO CREATE ICS FILE FOR GOOGLE')
                    return
                
                google_event = GoogleCalendarInterface.Parse_ICS(filename)
                # Check if can get any event from ICS
                if google_event == None:
                    messagebox.showerror(title=FAILED_TITLE, message=FAILED_ICS_PARSING)
                    return
                
                removed, reason = GoogleCalendarInterface.UpdateEvent(id=self.event_details['id'], update=google_event.event)
                if removed == False and reason == '':
                    messagebox.showerror(title=FAILED_TITLE, message=NO_GOOGLE_CONNECTION_MSG)
                    return False

            elif self.event_details['platform'] == OUTLOOK_CALENDAR:
                # create outlook event
                filename = EventsManager.CreateICSFileFromInput(input)
                if filename == None:
                    logging.error(f'[{__name__}] FAILED TO CREATE ICS FILE FOR OUTLOOK')
                    return
                
                outlook_event = outlook_interface.parse_ics(filename)
                # Check if can get any event from ICS
                if outlook_event == None:
                    messagebox.showerror(title=FAILED_TITLE, message=FAILED_ICS_PARSING)
                    return
                
                removed = None
                response = None
                try:
                    removed, response = outlook_interface.send_flask_req('update_event', json_data={'event_id':self.event_details['id'], 'event':outlook_event.event})
                except:
                    pass
                if removed == None and response == None:
                    messagebox.showerror(title=FAILED_TITLE, message=NO_OUTLOOK_CONNECTION_MSG)
                    return

            self.ChangeEntryState(state='disabled')

            # Update Local DB
            EventsManager.UpdateFromEventDB(id=self.event_details['id'], update=self.event_details, target=EventsManager.events_db)
            self.UpdateEntries()

            messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully Updated {self.event_details["name"]} on {self.event_details["platform"]} Calendar')
        except Exception as e:
            messagebox.showinfo(title=FAILED_TITLE, message=f'Failed update of {self.event_details["name"]} on {self.event_details["platform"]} Calendar\ndue to\n{e}')
    
    def PickDate(self, entry):
        date_window, cal, submit_btn = popup_mgr.CreateDateWindow()

        def GrabDate(entry, date:str, window):
            GUIInterface.UpdateEntry(entry, date)
            window.destroy()

        submit_btn.configure(command=lambda: GrabDate(entry, cal.get_date(), date_window))

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
    
    def RemoveCard(self, askBeforeDelete=True):
        self.remove_cb(self.index, askBeforeDelete)