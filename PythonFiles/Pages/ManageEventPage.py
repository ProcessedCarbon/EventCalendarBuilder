from Pages.Page import Page
from GUI.GUIInterface import GUIInterface

class ManageEventPage(Page):
    def __init__(self):
        super().__init__()

    def OnStart(self):
        rows = [1, 6, 1]
        cols = [1, 6, 1]
        self.PageGrid(rows=rows, cols=cols)

        label = GUIInterface.CreateLabel(text="Event Management", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        label.grid(row=0, column=1)

        content_frame = GUIInterface.CreateScrollableFrame(self.page, fg_color='blue')
        content_frame.grid(row=1, column=1, sticky='nsew')
