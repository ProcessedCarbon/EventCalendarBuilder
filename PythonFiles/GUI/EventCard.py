from GUI.GUIInterface import GUIInterface
from Events.EventsManager import EventsManager
import Calendar.CalendarMacInterface as cal_mac
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
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

        # date
        d_frame, d_label, d_entry = GUIInterface.CreateEntryWithLabel(label= "Date" + ":",
                                                                      entry_width=attribute_width, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(d_entry, str(event_details['date']))
        d_frame.grid(row=2, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # start time
        st_frame, st_label, st_entry = GUIInterface.CreateEntryWithLabel(label= "Start" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(st_entry, str(event_details['start_time']))
        st_frame.grid(row=3, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # start time
        et_frame, et_label, et_entry = GUIInterface.CreateEntryWithLabel(label= "End" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(et_entry, str(event_details['end_time']))
        et_frame.grid(row=4, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # platform
        p_frame, p_label, p_entry = GUIInterface.CreateEntryWithLabel(label= "Platform" + ":",
                                                                        entry_width=attribute_width, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(p_entry, str(event_details['platform']))
        p_frame.grid(row=5, column=0, sticky='nsew', padx=detail_gap, pady=detail_gap)

        # Remove event button
        remove_btn = GUIInterface.CreateButton(on_click=remove_cb, 
                                               text='Remove')
        remove_btn.grid(row=6, column=0, sticky='nsew')

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

        if self.platform == 'Google':
            removed = self.RemoveGoogle()
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
        success = GoogleCalendarInterface.DeleteEvent(self.id)
        return success

    def RemoveOutlook(self):
        pass