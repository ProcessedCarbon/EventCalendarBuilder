from Pages.Page import Page
from GUI.GUIInterface import GUIInterface

class ManageEventPage(Page):
    def __init__(self):
        super().__init__()

    def OnStart(self):
        label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=(20, 10))
