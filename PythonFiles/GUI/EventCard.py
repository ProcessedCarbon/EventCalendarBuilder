from GUI.GUIInterface import GUIInterface

class EventCard:
    def __init__(self, parent, row, col, event_details:dict, gap:int) -> None:
        tmp_frame = GUIInterface.current_frame
        self.details_frame = GUIInterface.CreateFrame(parent, fg_color='green')
        self.details_frame.grid(row=row, column=col, sticky='nsew', padx=gap, pady=gap)

        GUIInterface.CreateGrid(self.details_frame, rows=[1,6,1], cols=[1,6,1])

        # Details
        # title
        n_frame, n_label, n_entry = GUIInterface.CreateEntryWithLabel(label= "Name" + ":",
                                                                      entry_width=100, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(n_entry, str(event_details['name']))
        n_frame.grid(row=0, column=1, sticky='nsew')

        # location
        l_frame, l_label, l_entry = GUIInterface.CreateEntryWithLabel(label= "Location" + ":",
                                                                      entry_width=100, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(l_entry, str(event_details['location']))
        l_frame.grid(row=1, column=1, sticky='nsew')

        # date
        d_frame, d_label, d_entry = GUIInterface.CreateEntryWithLabel(label= "Date" + ":",
                                                                      entry_width=100, 
                                                                      entry_state='disabled')
        
        GUIInterface.UpdateEntry(d_entry, str(event_details['date']))
        d_frame.grid(row=2, column=1, sticky='nsew')

        # start time
        st_frame, st_label, st_entry = GUIInterface.CreateEntryWithLabel(label= "Start" + ":",
                                                                        entry_width=100, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(st_entry, str(event_details['start_time']))
        st_frame.grid(row=3, column=1, sticky='nsew')

        # start time
        et_frame, et_label, et_entry = GUIInterface.CreateEntryWithLabel(label= "End" + ":",
                                                                        entry_width=100, 
                                                                        entry_state='disabled')
        
        GUIInterface.UpdateEntry(et_entry, str(event_details['end_time']))
        et_frame.grid(row=4, column=1, sticky='nsew')

        GUIInterface.SetCurrentFrame(tmp_frame)