from GUI.GUIInterface import GUIInterface

class EventCard:
    def __init__(self, parent, row, col, event_details:dict, gap:int) -> None:

        # Variables
        tmp_frame = GUIInterface.current_frame

        self.card_frame = GUIInterface.CreateFrame(parent, fg_color='green')
        self.card_frame.grid(row=row, 
                                column=col, 
                                sticky='nsew', 
                                padx=gap, 
                                pady=gap,)
        GUIInterface.CreateGrid(self.card_frame, rows=[1] * len(event_details), cols=[1])
        self.card_frame.update()

        # Details Attributes
        attribute_width= self.card_frame.winfo_width() * 0.7
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
        remove_btn = GUIInterface.CreateButton(on_click=None, text='Remove')
        remove_btn.grid(row=6, column=0, sticky='nsew')

        GUIInterface.SetCurrentFrame(tmp_frame)

    def Destroy(self):
        self.card_frame.destroy()

    def RemoveEvent(self):
        pass

    def UpdateCalendar(self):
        pass

    def UpdateEventDB(self):
        pass