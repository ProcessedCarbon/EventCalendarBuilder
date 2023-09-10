from Pages.Page import Page
from GUI.GUIInterface import GUIInterface as gui
from Pages.MainPage import MainPage
from GUI.MainAppWindow import MainAppWindow
from GUI.CustomGUI import CustomGUI as c_gui
from Calendar.CalendarInterface import CalendarInterface
from Managers.TextProcessing import TextProcessingManager
from Managers.DateTimeManager import DateTimeManager

class SchedulePage(Page):
    def __init__(self):
        self.details_entries = {}
        self.detail_entry_width = MainAppWindow.app_width
        self.num_details = 7
        self.details_pady = 10
        self.filled = False
        super().__init__()

    def OnStart(self):
        self.PageGrid(rows=3, cols=3)

        # Back Button
        button = gui.CreateButton(text="<", on_click=lambda:self.SwitchPages(0))
        button.grid(row=0, column=0, sticky='nw')

        # Schedule Button
        schedue_btn = gui.CreateButton(text="Schedule",on_click=self.CreateICSUsingEntities)
        schedue_btn.grid(row=2, column=1, sticky='s', pady=10)

        # Title
        title = gui.CreateLabel(text="Schedule", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n')

        # Details
        details_frame = gui.CreateFrame(self.page)
        
        for i in range(self.num_details):
            details_frame.rowconfigure(i, weight=1)
        details_frame.grid(row=1, column=1, sticky='nsew', ipady=self.details_pady)

        # Details entry
        e_entry = c_gui.CreateEntryWithLabel(label="Event:", frame_row=0, entry_width=self.detail_entry_width)
        self.details_entries["Event"] = e_entry

        desp_entry = c_gui.CreateEntryWithLabel(label="Description:", frame_row=1,entry_width=self.detail_entry_width)
        self.details_entries["Description"] = desp_entry

        priorities = ["1", "2", "3", "4", "5"]
        priority_combo = gui.CreateComboBox(values=priorities)
        priority_combo.grid(row=2)
        self.details_entries["Priority"] = priority_combo

        l_entry = c_gui.CreateEntryWithLabel(label="Location:", frame_row=3,entry_width=self.detail_entry_width)
        self.details_entries["Location"] = l_entry

        d_entry = c_gui.CreateEntryWithLabel(label="Date:", frame_row=4,entry_width=self.detail_entry_width)
        self.details_entries["Date"] = d_entry

        st_entry = c_gui.CreateEntryWithLabel(label="Time Start:", frame_row=5,entry_width=self.detail_entry_width)
        self.details_entries["Start_Time"] = st_entry

        et_entry = c_gui.CreateEntryWithLabel(label="Time End:", frame_row=6,entry_width=self.detail_entry_width)
        self.details_entries["End_Time"] = et_entry

        self.UpdateDetails()

    def OnExit(self):
        MainPage.events = []
        self.filled = False
    
    def UpdateDetails(self):
        if len(MainPage.events) > 0 and self.filled == False:
            event = MainPage.events[0]

            time_list = event["TIME"]
            if len(time_list) < 2:
                new_time = DateTimeManager.AddToTime(time_list[0], hrs=1)
                time_list.append(new_time)

            gui.UpdateEntry(entry=self.details_entries["Event"], text_var=str(event["EVENT"]))
            gui.UpdateEntry(entry=self.details_entries["Location"], text_var=event["LOC"])
            gui.UpdateEntry(entry=self.details_entries["Date"], text_var=event["DATE"])
            gui.UpdateEntry(entry=self.details_entries["Start_Time"], text_var=time_list[0])
            gui.UpdateEntry(entry=self.details_entries["End_Time"], text_var=time_list[1])
            self.filled = True

        gui.root.after(500, self.UpdateDetails)  

    def getEmptyDetailCount(self)->int:
        count = 0
        for entry in self.details_entries:
            t = self.details_entries[entry].get()
            if t == "" or t == " ":
                count += 1
        return count

    def CreateICSUsingEntities(self):
        # Check if all inputs are empty
        empty_detail_entries = self.getEmptyDetailCount()

        if empty_detail_entries == self.num_details:
            print("No details provided!")
            return
        
        # Retrieve params from input
        date = self.details_entries["Date"].get()
        s_time = self.details_entries["Start_Time"].get()
        e_time = self.details_entries["End_Time"].get()
        desp = self.details_entries["Description"].get()
        priority = int(self.details_entries["Priority"].get())
        location = self.details_entries["Location"].get()
        event = self.details_entries["Event"].get()

        time_slots = []
        time_slots.append(s_time)
        time_slots.append(e_time)

        # Convert date and time to ics format
        ics_date = TextProcessingManager.ProcessDateToICSFormat(date)
        ics_time = TextProcessingManager.ProcessTimeToICSFormat(time_slots)
        ics_time_s, ics_time_e = TextProcessingManager.ProcessICS(ics_date, ics_time)

        # Create ICS File
        CalendarInterface.CreateICSEvent(e_name=event,
                                         e_description=desp,
                                         s_datetime=ics_time_s,
                                         e_datetime=ics_time_e,
                                         e_location=location,
                                         e_priority=int(priority))
        CalendarInterface.WriteToFile()
        CalendarInterface.ReadICSFile()



        
        
        

