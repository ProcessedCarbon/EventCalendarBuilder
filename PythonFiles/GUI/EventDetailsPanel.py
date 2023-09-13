from GUI.GUIInterface import GUIInterface as gui
from GUI.CustomGUI import CustomGUI as c_gui
from Managers.ErrorConfig import ErrorCodes
from Managers.ErrorConfig import getParamValFromKwarg
from GUI.MainAppWindow import MainAppWindow

class EventDetailsPanel:
    num_details = 7
    def __init__(self, parent, entry_widths:int, ipady:int=10, **grid_params):
        self.detail_entry_width = 180
        self.details_pady = ipady
        self.parent = parent
        self.grid_params = grid_params

        self.details_entries = {}
        self.detail_entries_values = {}
        self.filled = False
        self.details_frame = None

        self.GUI()
        
    def GUI(self):
        tmp_frame = gui.current_frame
        self.details_frame = gui.CreateFrame(self.parent, 
                                             fg_color='gray',
                                            #  width=MainAppWindow.app_width*0.2,
                                            #  height=MainAppWindow.app_height*0.2
                                             )

        for i in range(EventDetailsPanel.num_details):
            self.details_frame.rowconfigure(i, weight=1)

        row = getParamValFromKwarg("row", self.grid_params, default=0)
        column = getParamValFromKwarg("column", self.grid_params, default=0)
        sticky = getParamValFromKwarg("sticky", self.grid_params, default='nsew')
        self.details_frame.grid(row=row, column=column, sticky=sticky, ipady=self.details_pady)
       #self.details_frame.grid_propagate(0)

        # GUI
        e_frame = self.CreateEntryDetail(self.detail_entry_width, entryname="Event")
        e_frame.grid(row=0, sticky='nsew')

        desp_frame = self.CreateEntryDetail(self.detail_entry_width, entryname="Description")
        desp_frame.grid(row=1, sticky='nsew')

        priorities = ["1", "2", "3", "4", "5"]
        prio_frame = self.CreateDropdownDetail(values=priorities, entryname="Priority")
        prio_frame.grid(row=2, sticky='nsew')

        l_frame = self.CreateEntryDetail(self.detail_entry_width, entryname="Location")
        l_frame.grid(row=3, sticky='nsew')

        d_frame = self.CreateEntryDetail(self.detail_entry_width, entryname="Date")
        d_frame.grid(row=4,sticky='nsew')

        st_frame = self.CreateEntryDetail(self.detail_entry_width, entryname="Start Time")
        st_frame.grid(row=5,sticky='nsew')

        et_frame = self.CreateEntryDetail(self.detail_entry_width, entryname="End Time")
        et_frame.grid(row=6,sticky='nsew')

        gui.SetCurrentFrame(tmp_frame)

    def UpdateDetails(self, **kwargs):
        if kwargs == self.detail_entries_values == {} or len(kwargs) == len(self.detail_entries_values) == 0:
            ErrorCodes.PrintCustomError("No updates!")
            return
        
        for param in kwargs:
            if param not in self.details_entries:
                ErrorCodes.PrintErrorWithCode(1000)
                return

        self.detail_entries_values.update(kwargs)            

        gui.UpdateEntry(self.details_entries["Event"], self.detail_entries_values["Event"])
        gui.UpdateEntry(self.details_entries["Location"], self.detail_entries_values["Location"])
        gui.UpdateEntry(self.details_entries["Date"], self.detail_entries_values["Date"])
        gui.UpdateEntry(self.details_entries["Start_Time"], self.detail_entries_values["Start_Time"])
        gui.UpdateEntry(self.details_entries["End_Time"], self.detail_entries_values["End_Time"])
        self.filled = True

    def getEmptyDetailCount(self)->int:
        count = 0
        for entry in self.details_entries:
            t = self.details_entries[entry].get()
            if t == "" or t == " ":
                count += 1
        return count
    
    def Reset(self):
        self.detail_entries_values = {}
        self.filled = False

        gui.UpdateEntry(self.details_entries["Event"], "")
        gui.UpdateEntry(self.details_entries["Location"], "")
        gui.UpdateEntry(self.details_entries["Date"], "")
        gui.UpdateEntry(self.details_entries["Start_Time"], "")
        gui.UpdateEntry(self.details_entries["End_Time"], "")

    def Destroy(self):
        self.details_frame.destroy()
    
    # Create GUI
    def CreateEntryDetail(self, width:int, entryname:str):
        key = self.ConvertEntryNameToKey(entryname)
        e_frame, e_label, e_entry = c_gui.CreateEntryWithLabel(label= entryname + ":",entry_width=width)
        self.details_entries[key] = e_entry
        return e_frame

    def CreateDropdownDetail(self, values:list[str], entryname:str):
        key = self.ConvertEntryNameToKey(entryname)
        dropdown_frame, dropdown_label, dropdown_box = c_gui.CreateComboboxWithLabel(label=entryname +":", dropdown=values)
        self.details_entries[key] = dropdown_box
        return dropdown_frame
    
    def ConvertEntryNameToKey(self, name:str):
        return name.replace(" ", "_")