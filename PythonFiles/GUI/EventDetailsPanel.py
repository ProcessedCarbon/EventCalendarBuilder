from GUI.GUIInterface import GUIInterface
from Managers.ErrorConfig import getParamValFromKwarg
from Events.EventsManager import Event
from Events.EventsManager import EventsManager

class EventDetailsPanel:
    num_details = 7
    def __init__(self, parent, event:Event, remove_callback,index:int, gap:int=10, **grid_params):
        self.detail_entry_width = 180
        self.gap = gap
        self.parent = parent
        self.grid_params = grid_params

        self.details_entries = {}
        self.filled = False
        self.details_frame = None
        self.event = event
        self.remove_callback = remove_callback
        self.index = index

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
        for i in range(EventDetailsPanel.num_details):
            self.details_frame.rowconfigure(i, weight=1)
        
        # Columns
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.columnconfigure(1, weight=10)
        self.details_frame.columnconfigure(2, weight=1)

        # GUI
        remove_btn = GUIInterface.CreateButton(on_click=self.OnRemove, text='X', width=50)
        remove_btn.grid(row=0, column=2, pady=10)

        e_frame, e_entry = self.CreateEntryDetail(self.detail_entry_width, entryname="Event")
        e_frame.grid(row=1, column=1,sticky='nsew', pady=self.gap)

        desp_frame, desp_entry = self.CreateEntryDetail(self.detail_entry_width, entryname="Description")
        desp_frame.grid(row=2, column=1, sticky='nsew',pady=self.gap)

        priorities = ["1", "2", "3", "4", "5"]
        prio_frame = self.CreateDropdownDetail(values=priorities, entryname="Priority")
        prio_frame.grid(row=3, column=1, sticky='nsew',pady=self.gap)

        l_frame, l_entry = self.CreateEntryDetail(self.detail_entry_width, entryname="Location")
        l_frame.grid(row=4, column=1, sticky='nsew',pady=self.gap)

        d_frame, d_entry = self.CreateEntryDetail(self.detail_entry_width, entryname="Date")
        d_frame.grid(row=5, column=1,sticky='nsew',pady=self.gap)
        d_entry.bind('<1>', lambda event, entry=d_entry: self.PickDate(entry))

        st_frame, st_entry = self.CreateEntryDetail(self.detail_entry_width, entryname="Start Time")
        st_frame.grid(row=6, column=1,sticky='nsew',pady=self.gap)

        et_frame, et_entry = self.CreateEntryDetail(self.detail_entry_width, entryname="End Time")
        et_frame.grid(row=7, column=1,sticky='nsew',pady=self.gap)

        GUIInterface.SetCurrentFrame(tmp_frame)

    def UpdateEventWithDetails(self):
        details = self.getDetails()
        self.event.setName(details['Event'])
        self.event.setLocation(details['Location'])
        self.event.setDate(details['Date'])
        self.event.setStart_Time(details['Start_Time'])
        self.event.setEnd_Time(details['End_Time'])

    def UpdateDetails(self):
        GUIInterface.UpdateEntry(self.details_entries["Event"], self.event.getName())
        GUIInterface.UpdateEntry(self.details_entries["Location"], self.event.getLocation())
        GUIInterface.UpdateEntry(self.details_entries["Date"], self.event.getDate(), uneditable=True)
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], self.event.getStart_Time(), uneditable=True)
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], self.event.getEnd_Time(), uneditable=True)
        self.filled = True

    def getEmptyDetailCount(self)->int:
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
        GUIInterface.UpdateEntry(self.details_entries["Date"], "")
        GUIInterface.UpdateEntry(self.details_entries["Start_Time"], "")
        GUIInterface.UpdateEntry(self.details_entries["End_Time"], "")

    def Destroy(self):
        self.details_frame.destroy()
    
    # Create GUI
    def CreateEntryDetail(self, width:int, entryname:str):
        key = self.ConvertEntryNameToKey(entryname)
        e_frame, e_label, e_entry = GUIInterface.CreateEntryWithLabel(label= entryname + ":",entry_width=width)
        self.details_entries[key] = e_entry
        return e_frame, e_entry

    def CreateDropdownDetail(self, values:list[str], entryname:str):
        key = self.ConvertEntryNameToKey(entryname)
        dropdown_frame, dropdown_label, dropdown_box = GUIInterface.CreateComboboxWithLabel(label=entryname +":", dropdown=values)
        self.details_entries[key] = dropdown_box
        return dropdown_frame
    
    def ConvertEntryNameToKey(self, name:str):
        return name.replace(" ", "_")
    
    def getDetails(self)->dict:
        details = {}
        for detail in self.details_entries:
            details[detail] = self.details_entries[detail].get()
        return details
    
    def getEvent(self):
        return self.event
    
    def OnRemove(self):
        EventsManager.RemoveEvent(id=self.event.getId())
        self.remove_callback(self.index)
        self.Destroy()
    
    def PickDate(self, entry):
        date_window, cal, submit_btn = GUIInterface.CreateDateWindow()
        submit_btn.configure(command=lambda:self.GrabDate(entry, cal.get_date(), date_window))

    def GrabDate(self, entry, date:str, window):
        GUIInterface.UpdateEntry(entry, date, uneditable=True)
        window.destroy()
