from GUI.GUIInterface import GUIInterface
from Events.EventsManager import EventsManager
import Calendar.CalendarMacInterface as cal_mac
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface

from sys import platform
import subprocess

class EventCard:
    def __init__(self, parent, row, col, event_details:dict, gap:int, remove_cb) -> None:

        # Variables
        tmp_frame = GUIInterface.current_frame
        self.id = event_details['id']
        self.platform = event_details['platform']
        self.name = event_details['name']

        self.card_frame = GUIInterface.CreateFrame(parent, fg_color='green')
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
        
        GUIInterface.UpdateEntry(n_entry, str(event_details['name']))
        n_frame.grid(row=0, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # location
        l_frame, l_label, l_entry = GUIInterface.CreateEntryWithLabel(label= "Location" + ":",
                                                                      entry_width=attribute_width, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(l_entry, str(event_details['location']))
        l_frame.grid(row=1, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # start date
        s_d_frame, s_d_label, s_d_entry = GUIInterface.CreateEntryWithLabel(label= "Start Date" + ":",
                                                                      entry_width=attribute_width, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(s_d_entry, str(event_details['s_date']))
        s_d_frame.grid(row=2, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # end date
        e_d_frame, e_d_label, e_d_entry = GUIInterface.CreateEntryWithLabel(label= "End Date" + ":",
                                                                      entry_width=attribute_width, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(e_d_entry, str(event_details['e_date']))
        e_d_frame.grid(row=3, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # start time
        st_frame, st_label, st_entry = GUIInterface.CreateEntryWithLabel(label= "Start" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(st_entry, str(event_details['start_time']))
        st_frame.grid(row=4, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # end time
        et_frame, et_label, et_entry = GUIInterface.CreateEntryWithLabel(label= "End" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(et_entry, str(event_details['end_time']))
        et_frame.grid(row=5, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # platform
        p_frame, p_label, p_entry = GUIInterface.CreateEntryWithLabel(label= "Platform" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(p_entry, str(event_details['platform']))
        p_frame.grid(row=6, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # recurrence
        r_frame, r_label, r_entry = GUIInterface.CreateEntryWithLabel(label= "Recurrence" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(r_entry, str(event_details['recurring']))
        r_frame.grid(row=7, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # Remove event button
        remove_btn = GUIInterface.CreateButton(on_click=remove_cb, 
                                               text='Remove')
        remove_btn.grid(row=8, column=0, sticky='nsew')

        GUIInterface.SetCurrentFrame(tmp_frame)

    def Destroy(self)->bool:
        removed_from_cal = self.RemoveFromCalender()

        if removed_from_cal:
            success = EventsManager.RemoveFromEventDB(self.id, EventsManager.events_db)
            if success:
                EventsManager.WriteEventDBToJSON()
                self.card_frame.destroy()
                return True
        return False

    def RemoveFromCalender(self)->bool:
        if self.platform == 'Default':
            self.RemoveDefault()
            return True
        
        elif self.platform == 'Google':
            removed = self.RemoveGoogle()
            return removed == True
        
        elif self.platform == 'Outlook':
            removed = self.RemoveOutlook()
            return removed == True
        
        return False
    
    def RemoveDefault(self):
        if platform == "linux":
            #subprocess.run(['xdg-open', file])
            pass
        elif platform == 'darwin':
            cal_mac.RemoveMacCalendarEvents(self.name)
        else:
            #os.startfile(file)
            pass
    
    def RemoveGoogle(self)->bool:
        return GoogleCalendarInterface.DeleteEvent(self.id)

    def RemoveOutlook(self)->bool:
        removed, response = outlook_interface.send_flask_req('delete_event', json_data={'event_id':self.id})
        return removed
