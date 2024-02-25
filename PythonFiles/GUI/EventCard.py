from tkinter import messagebox
from sys import platform

from GUI.GUIInterface import GUIInterface
from Events.EventsManager import EventsManager
import Calendar.CalendarMacInterface as cal_mac
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
from Calendar.CalendarConstants import DEFAULT_CALENDAR, OUTLOOK_CALENDAR, GOOGLE_CALENDAR

class EventCard:
    def __init__(self, parent, row, col, event_details:dict, gap:int, remove_cb, index:int) -> None:

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
                                column=col, 
                                sticky='nsew', 
                                padx=gap, 
                                pady=gap,)
        GUIInterface.CreateGrid(self.card_frame, rows=[1] * len(event_details), cols=[1])
        self.card_frame.update()

        # Details Attributes
        attribute_width= self.card_frame.winfo_width() * 0.6
        detail_gap = 5

        # Details
        # title
        n_frame, n_label, n_entry = GUIInterface.CreateEntryWithLabel(label= "Name" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        n_entry.configure(fg_color=frame_color, border_color = frame_color, text_color=text_color)
        GUIInterface.UpdateEntry(n_entry, str(event_details['name']))
        n_frame.grid(row=0, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # desc
        desc_frame, desc_label, desc_entry = GUIInterface.CreateEntryWithLabel(label= "Description" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        desc_entry.configure(fg_color=frame_color, border_color = frame_color, text_color=text_color)
        GUIInterface.UpdateEntry(desc_entry, str(event_details['description']))
        desc_frame.grid(row=1, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # location
        l_frame, l_label, l_entry = GUIInterface.CreateEntryWithLabel(label= "Location" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        
        GUIInterface.UpdateEntry(l_entry, str(event_details['location']))
        l_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        l_frame.grid(row=2, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # start date
        s_d_frame, s_d_label, s_d_entry = GUIInterface.CreateEntryWithLabel(label= "Start Date" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        
        GUIInterface.UpdateEntry(s_d_entry, str(event_details['s_date']))
        s_d_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        s_d_frame.grid(row=3, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # end date
        e_d_frame, e_d_label, e_d_entry = GUIInterface.CreateEntryWithLabel(label= "End Date" + ":",
                                                                    entry_width=attribute_width, 
                                                                    entry_state='disabled')
        
        GUIInterface.UpdateEntry(e_d_entry, str(event_details['e_date']))
        e_d_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        e_d_frame.grid(row=4, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # start time
        st_frame, st_label, st_entry = GUIInterface.CreateEntryWithLabel(label= "Start" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(st_entry, str(event_details['start_time']))
        st_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        st_frame.grid(row=5, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # end time
        et_frame, et_label, et_entry = GUIInterface.CreateEntryWithLabel(label= "End" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(et_entry, str(event_details['end_time']))
        et_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        et_frame.grid(row=6, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # platform
        p_frame, p_label, p_entry = GUIInterface.CreateEntryWithLabel(label= "Platform" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(p_entry, str(event_details['platform']))
        p_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        p_frame.grid(row=7, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # recurrence
        r_frame, r_label, r_entry = GUIInterface.CreateEntryWithLabel(label= "Recurrence" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(r_entry, str(event_details['recurring']))
        r_entry.configure(fg_color=frame_color, border_color = frame_color,text_color=text_color)
        r_frame.grid(row=8, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # Remove event button
        remove_btn = GUIInterface.CreateButton(on_click=lambda:self.remove_cb(index), 
                                            text='Remove')
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

            messagebox.showinfo(title='Success', message=f'Successfully removed {self.name} from {self.platform} Calendar')
            return True            
        except:
            messagebox.showinfo(title='Failed', message=f'Failed removal of {self.name}')
            return False
