from tkinter import messagebox
from sys import platform

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import SUCCESS_TITLE, EVENT_ROW_GAP, EVENT_DETAILS_PANEL_CARD_GAP, EVENT_DETAILS_CARD_ENTRY_WIDTH_MODIFIER, FAILED_TITLE
from Events.EventsManager import EventsManager
import Calendar.CalendarMacInterface as cal_mac
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
from Calendar.CalendarConstants import DEFAULT_CALENDAR, OUTLOOK_CALENDAR, GOOGLE_CALENDAR

class EventCard:
    def __init__(self, parent, row, event_details:dict, gap:int, remove_cb, index:int) -> None:

        # Variables
        tmp_frame = GUIInterface.current_frame
        self.id = event_details['id']
        self.platform = event_details['platform']
        self.name = event_details['name']
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
        n_frame, n_label, n_entry = GUIInterface.CreateEntryWithLabel(label= "Name" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        n_entry.configure(fg_color=frame_color, border_color = frame_color, text_color=text_color)

        # desc
        desc_frame, desc_label, desc_entry = GUIInterface.CreateEntryWithLabel(label= "Description" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        desc_entry.configure(fg_color=frame_color, border_color = frame_color, text_color=text_color)

        # location
        l_frame, l_label, l_entry = GUIInterface.CreateEntryWithLabel(label= "Location" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        
        l_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # start date
        s_d_frame, s_d_label, s_d_entry = GUIInterface.CreateEntryWithLabel(label= "Start Date" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        
        s_d_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # end date
        e_d_frame, e_d_label, e_d_entry = GUIInterface.CreateEntryWithLabel(label= "End Date" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        
        e_d_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # start time
        st_frame, st_label, st_entry = GUIInterface.CreateEntryWithLabel(label= "Start" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        st_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # end time
        et_frame, et_label, et_entry = GUIInterface.CreateEntryWithLabel(label= "End" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        et_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # platform
        p_frame, p_label, p_entry = GUIInterface.CreateEntryWithLabel(label= "Platform" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        p_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # recurrence
        r_frame, r_label, r_entry = GUIInterface.CreateEntryWithLabel(label= "Recurrence" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        r_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)

        # Remove event button
        remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(index), 
                                            text='Remove')
        
        # Update entries
        GUIInterface.UpdateEntry(n_entry, str(event_details['name']))
        GUIInterface.UpdateEntry(desc_entry, str(event_details['description']))
        GUIInterface.UpdateEntry(l_entry, str(event_details['location']))
        GUIInterface.UpdateEntry(s_d_entry, str(event_details['s_date']))
        GUIInterface.UpdateEntry(e_d_entry, str(event_details['e_date']))
        GUIInterface.UpdateEntry(st_entry, str(event_details['start_time']))
        GUIInterface.UpdateEntry(et_entry, str(event_details['end_time']))
        GUIInterface.UpdateEntry(p_entry, str(event_details['platform']))
        GUIInterface.UpdateEntry(r_entry, str(event_details['recurring']))

        # Grid GUI
        n_frame.grid(row=0, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        desc_frame.grid(row=1, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        l_frame.grid(row=2, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        s_d_frame.grid(row=3, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        e_d_frame.grid(row=4, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        st_frame.grid(row=5, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        et_frame.grid(row=6, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        p_frame.grid(row=7, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        r_frame.grid(row=8, column=0, sticky='nsew', padx=EVENT_DETAILS_PANEL_CARD_GAP, pady=EVENT_DETAILS_PANEL_CARD_GAP)
        remove_btn.grid(row=9, column=0)

        GUIInterface.current_frame = tmp_frame

    def Destroy(self)->bool:
        removed_from_cal = self.RemoveFromCalender()
        if removed_from_cal:
            success = EventsManager.RemoveFromEventDB(self.id, EventsManager.events_db)
            if success:
                self.card_frame.destroy()
                return True
        return False

    def RemoveFromCalender(self)->bool:
        try:
            if self.platform == DEFAULT_CALENDAR: # Should not occur as Default calendar methods are not saved locally
                if platform == 'darwin': 
                    cal_mac.RemoveMacCalendarEvents(self.name)
                else: 
                    removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.id})
            
            elif self.platform == GOOGLE_CALENDAR:
                removed, reason = GoogleCalendarInterface.DeleteEvent(self.id)
            
            elif self.platform == OUTLOOK_CALENDAR:
                removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.id})

            messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully removed {self.name} from {self.platform} Calendar')
            return True            
        except:
            messagebox.showinfo(title=FAILED_TITLE, message=f'Failed removal of {self.name}')
            return False
