from tkinter import messagebox
from sys import platform
import logging

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import SUCCESS_TITLE, EVENT_ROW_GAP, EVENT_DETAILS_PANEL_CARD_GAP, EVENT_DETAILS_CARD_ENTRY_WIDTH_MODIFIER, FAILED_TITLE, WARNING_TITLE
from Events.EventsManager import EventsManager
import Calendar.CalendarMacInterface as cal_mac
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
from Calendar.CalendarConstants import DEFAULT_CALENDAR, OUTLOOK_CALENDAR, GOOGLE_CALENDAR
from Calendar.CalendarInterface import CalendarInterface

class EventCard:
    def __init__(self, parent, row, event_details:dict, remove_cb, index:int) -> None:

        # Variables
        tmp_frame = GUIInterface.current_frame
        self.event_details = event_details
        self.index = index
        self.remove_cb = remove_cb
        frame_color = GUIInterface.color_palette['CTkFrame']['border_color'][0]
        text_color = GUIInterface.color_palette['CTkLabel']['text_color'][0]

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
        # title
        self.n_frame,  self.n_label, self.n_entry = GUIInterface.CreateEntryWithLabel(label= "Name:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')
        self.n_entry.configure(fg_color=frame_color, border_color = frame_color, text_color=text_color)

        # desc
        self.desc_frame, self.desc_label, self.desc_entry = GUIInterface.CreateEntryWithLabel(label= "Description:",
                                                                                            entry_width=attribute_width, 
                                                                                            entry_state='normal')
        self.desc_entry.configure(fg_color=frame_color, border_color = frame_color, text_color=text_color)

        # location
        self.l_frame, self.l_label, self.l_entry = GUIInterface.CreateEntryWithLabel(label= "Location:",
                                                                                    entry_width=attribute_width, 
                                                                                    entry_state='disabled')
        
        self.l_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # start date
        self.s_d_frame, self.s_d_label, self.s_d_entry = GUIInterface.CreateEntryWithLabel(label= "Start Date:",
                                                                                            entry_width=attribute_width, 
                                                                                            entry_state='disabled')
        
        self.s_d_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # end date
        self.e_d_frame, self.e_d_label, self.e_d_entry = GUIInterface.CreateEntryWithLabel(label= "End Date:",
                                                                                            entry_width=attribute_width, 
                                                                                            entry_state='disabled')
        
        self.e_d_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # start time
        self.st_frame, self.st_label, self.st_entry = GUIInterface.CreateEntryWithLabel(label= "Start Time:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')
        
        self.st_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # end time
        self.et_frame, self.et_label, self.et_entry = GUIInterface.CreateEntryWithLabel(label= "End Time:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')
        
        self.et_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # platform
        self.p_frame, self.p_label, self.p_entry = GUIInterface.CreateEntryWithLabel(label= "Platform:",
                                                                                    entry_width=attribute_width, 
                                                                                    entry_state='disabled')
        
        self.p_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # recurrence
        self.r_frame, self.r_label, self.r_entry = GUIInterface.CreateEntryWithLabel(label= "Repeated:",
                                                                                    entry_width=attribute_width, 
                                                                                    entry_state='disabled')
        
        self.r_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # timezone
        self.tz_frame, self.tz_label, self.tz_entry = GUIInterface.CreateEntryWithLabel(label= "Timezone:",
                                                                                        entry_width=attribute_width, 
                                                                                        entry_state='disabled')
        
        self.tz_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # Buttons
        self.remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(index), 
                                                    text='Remove')
        self.update_btn = GUIInterface.CreateButton(on_click=self.UpdateOnCalendar, 
                                                    text='Update')
        
        # Update entries
        self.UpdateEntries()

        # Grid GUI
        self.n_frame.grid(row=0, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.desc_frame.grid(row=1, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.l_frame.grid(row=2, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.s_d_frame.grid(row=3, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.e_d_frame.grid(row=4, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.st_frame.grid(row=5, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.et_frame.grid(row=6, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.p_frame.grid(row=7, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.r_frame.grid(row=8, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.tz_frame.grid(row=9, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        self.remove_btn.grid(row=10, column=0)
        self.update_btn.grid(row=10, column=1)

        GUIInterface.current_frame = tmp_frame

    def Destroy(self)->bool:
        removed_from_cal = self.RemoveFromCalender()
        if removed_from_cal:
            success = EventsManager.RemoveFromEventDB(self.event_details['id'], EventsManager.events_db)
            if success:
                self.card_frame.destroy()
                return True
        return False

    def UpdateEntries(self):
        GUIInterface.UpdateEntry(self.n_entry, self.event_details['name'])
        GUIInterface.UpdateEntry(self.desc_entry, self.event_details['description'])
        GUIInterface.UpdateEntry(self.l_entry, self.event_details['location'])
        GUIInterface.UpdateEntry(self.s_d_entry, self.event_details['s_date'])
        GUIInterface.UpdateEntry(self.e_d_entry, self.event_details['e_date'])
        GUIInterface.UpdateEntry(self.st_entry, self.event_details['start_time'])
        GUIInterface.UpdateEntry(self.et_entry, self.event_details['end_time'])
        GUIInterface.UpdateEntry(self.p_entry, self.event_details['platform'])
        GUIInterface.UpdateEntry(self.r_entry, self.event_details['recurring'])
        GUIInterface.UpdateEntry(self.tz_entry, self.event_details['timezone'])
    
    def UpdateEventDetails(self):
        self.event_details['name'] = self.n_entry.get()
        self.event_details['description'] = self.desc_entry.get()
        self.event_details['location'] = self.l_entry.get()
        self.event_details['s_date'] = self.s_d_entry.get()
        self.event_details['e_date'] = self.e_d_entry.get()
        self.event_details['start_time'] = self.st_entry.get()
        self.event_details['end_time'] = self.et_entry.get()
        self.event_details['platform'] = self.p_entry.get()
        self.event_details['recurring'] = self.r_entry.get()

    def RemoveFromCalender(self)->bool:
        try:
            if self.event_details['platform'] == DEFAULT_CALENDAR: # Should not occur as Default calendar methods are not saved locally
                if platform == 'darwin': 
                    cal_mac.RemoveMacCalendarEvents(self.event_details['name'])
                else: 
                    removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.event_details['id']})
            
            elif self.event_details['platform'] == GOOGLE_CALENDAR:
                removed, reason = GoogleCalendarInterface.DeleteEvent(self.event_details['id'])
            
            elif self.event_details['platform'] == OUTLOOK_CALENDAR:
                removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.event_details['id']})

            messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully removed {self.event_details['name']} from {self.event_details['platform']} Calendar')
            return True            
        except:
            messagebox.showinfo(title=FAILED_TITLE, message=f'Failed removal of {self.event_details['name']}')
            return False
        
    def UpdateOnCalendar(self):
        try:
            self.UpdateEventDetails()
            input = {
                'Event': self.event_details['name'],
                'Description': self.event_details['description'],
                'Location': self.event_details['location'],
                'Start_Date': self.event_details['s_date'],
                'End_Date': self.event_details['e_date'],
                'Start_Time': self.event_details['start_time'],
                'End_Time': self.event_details['end_time'],
                'Timezone': 'Asia/Singapore',
                'Repeated': self.event_details['recurring'],
                'Platform': self.event_details['platform'],
            }

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
                    return ''
                google_event = GoogleCalendarInterface.Parse_ICS(filename).event
                removed, reason = GoogleCalendarInterface.UpdateEvent(id=self.event_details['id'], update=google_event)
            
            elif self.event_details['platform'] == OUTLOOK_CALENDAR:
                # create outlook event
                filename = EventsManager.CreateICSFileFromInput(input)
                if filename == None:
                    logging.error(f'[{__name__}] FAILED TO CREATE ICS FILE FOR OUTLOOK')
                    return ''
                outlook_event = outlook_interface.parse_ics(filename).event
                removed, response = outlook_interface.send_flask_req('update_event', json_data={'event_id':self.event_details['id'], 'event':outlook_event})

            # Update Local DB
            EventsManager.UpdateFromEventDB(id=self.event_details['id'], update=self.event_details, target=EventsManager.events_db)
            self.UpdateEntries()
            messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully Updated {self.event_details['name']} on {self.event_details['platform']} Calendar')
        except Exception as e:
            messagebox.showinfo(title=FAILED_TITLE, message=f'Failed update of {self.event_details['name']} on {self.event_details['platform']} Calendar\ndue to\n{e}')