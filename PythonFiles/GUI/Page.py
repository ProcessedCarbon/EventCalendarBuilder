from GUI.GUIInterface import GUIInterface
from Managers.ErrorConfig import ErrorCodes
from GUI.MainAppWindow import MainAppWindow

class Page:
    pages = []
    current_page = None

    def __init__(self):
        if GUIInterface.root == None:
            ErrorCodes.PrintErrorWithCode(1003)
            return

        self.page = GUIInterface.CreateFrame(GUIInterface.root)
        self.page.grid(row=0, column=0, sticky="nsew")
        Page.pages.append(self.page)
        self.OnStart()
        GUIInterface.ClearCurrentFrame()

    def OnStart(self):
        pass

    def OnExit(self):
        pass

    def PageGrid(self, rows=1, cols=1):
        GUIInterface.CreateGrid(self.page, rows=rows, cols=cols)

    def SwitchPages(self, page:int=0):
        if len(Page.pages) < 1:
            ErrorCodes.PrintErrorWithCode(1002)
            return
        
        if page > len(Page.pages) - 1:
            ErrorCodes.PrintErrorWithCode(1003)
            return
                
        self.OnExit()
        Page.current_page = Page.pages[page]
        Page.current_page.tkraise()
