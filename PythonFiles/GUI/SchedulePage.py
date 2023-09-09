from GUI.Page import Page
from GUI.GUIInterface import GUIInterface as gui
from GUI.MainPage import MainPage
from GUI.MainAppWindow import MainAppWindow

class SchedulePage(Page):
    def __init__(self):
        self.details_entries = {}
        self.detail_entry_width = MainAppWindow.app_width
        self.num_details = 7
        self.details_pady = 10
        super().__init__()

    def OnStart(self):
        self.PageGrid(rows=3, cols=3)

        # Back Button
        button = gui.CreateButton(text="<", on_click=lambda:self.SwitchPages(0))
        button.grid(row=0, column=0, sticky='nw')

        # Title
        title = gui.CreateLabel(text="Schedule", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n')

        details_frame = gui.CreateFrame(self.page)

        for i in range(self.num_details):
            details_frame.rowconfigure(i, weight=1)
        details_frame.grid(row=1, column=1, sticky='nsew', ipady=self.details_pady)

        # Details entry
        e_entry = gui.CreateEntryWithLabel(frame_target=details_frame, label="Event:", frame_row=0, entry_width=self.detail_entry_width)
        self.details_entries["Event"] = e_entry

        gui.CreateEntryWithLabel(frame_target=details_frame, label="Description:", frame_row=1,entry_width=self.detail_entry_width)
        gui.CreateEntryWithLabel(frame_target=details_frame, label="Priority:", frame_row=2,entry_width=self.detail_entry_width)

        l_entry = gui.CreateEntryWithLabel(frame_target=details_frame, label="Location:", frame_row=3,entry_width=self.detail_entry_width)
        self.details_entries["Location"] = l_entry

        d_entry = gui.CreateEntryWithLabel(frame_target=details_frame, label="Date:", frame_row=4,entry_width=self.detail_entry_width)
        self.details_entries["Date"] = d_entry

        st_entry = gui.CreateEntryWithLabel(frame_target=details_frame, label="Time Start:", frame_row=5,entry_width=self.detail_entry_width)
        self.details_entries["Start_Time"] = st_entry

        et_entry = gui.CreateEntryWithLabel(frame_target=details_frame, label="Time End:", frame_row=6,entry_width=self.detail_entry_width)
        self.details_entries["End_Time"] = et_entry

        self.UpdateDetails()

    def UpdateDetails(self):
        if len(MainPage.events) > 0:
            event = MainPage.events[0]
            gui.UpdateEntry(entry=self.details_entries["Event"], text_var=str(event["EVENT"]))
            gui.UpdateEntry(entry=self.details_entries["Location"], text_var=event["LOC"])
            gui.UpdateEntry(entry=self.details_entries["Date"], text_var=event["DATE"])
            gui.UpdateEntry(entry=self.details_entries["Start_Time"], text_var=event["TIME"][0])
            gui.UpdateEntry(entry=self.details_entries["End_Time"], text_var=event["TIME"][1])
            MainPage.events.clear()
            print("Filled!")
        gui.root.after(500, self.UpdateDetails)  
