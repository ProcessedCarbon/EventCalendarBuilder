from GUI.GUIInterface import GUIInterface as gui
from GUI.CustomGUI import CustomGUI as c_gui
from Managers.ErrorConfig import ErrorCodes
from Managers.ErrorConfig import getParamValFromKwarg

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
        self.details_frame = gui.CreateFrame(self.parent, fg_color='gray')

        for i in range(EventDetailsPanel.num_details):
            self.details_frame.rowconfigure(i, weight=1)

        row = getParamValFromKwarg("row", self.grid_params, default=0)
        column = getParamValFromKwarg("column", self.grid_params, default=0)
        sticky = getParamValFromKwarg("sticky", self.grid_params, default='nsew')
        self.details_frame.grid(row=row, column=column, sticky=sticky, ipady=self.details_pady)

        # GUI
        e_frame, e_label, e_entry = c_gui.CreateEntryWithLabel(label="Event:",entry_width=self.detail_entry_width)
        e_frame.grid(row=0, sticky='nsew')
        self.details_entries["Event"] = e_entry

        desp_frame, desp_label, desp_entry = c_gui.CreateEntryWithLabel(label="Description:", entry_width=self.detail_entry_width)
        desp_frame.grid(row=1, sticky='nsew')
        self.details_entries["Description"] = desp_entry

        priorities = ["1", "2", "3", "4", "5"]
        prio_frame, prio_label, prio_box = c_gui.CreateComboboxWithLabel(label="Priority:", dropdown=priorities)
        prio_frame.grid(row=2, sticky='nsew')
        self.details_entries["Priority"] = prio_box

        l_frame, l_label,l_entry = c_gui.CreateEntryWithLabel(label="Location:", entry_width=self.detail_entry_width)
        l_frame.grid(row=3, sticky='nsew')
        self.details_entries["Location"] = l_entry

        d_frame, d_label, d_entry = c_gui.CreateEntryWithLabel(label="Date:",entry_width=self.detail_entry_width)
        d_frame.grid(row=4,sticky='nsew')
        self.details_entries["Date"] = d_entry

        st_frame, st_label, st_entry = c_gui.CreateEntryWithLabel(label="Time Start:", entry_width=self.detail_entry_width)
        st_frame.grid(row=5,sticky='nsew')
        self.details_entries["Start_Time"] = st_entry

        et_frame, et_label, et_entry = c_gui.CreateEntryWithLabel(label="Time End:",entry_width=self.detail_entry_width)
        et_frame.grid(row=6,sticky='nsew')
        self.details_entries["End_Time"] = et_entry

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
    