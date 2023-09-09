from GUI.GUIInterface import GUIInterface as gui
from Managers.ErrorConfig import ErrorCodes
from GUI.MainAppWindow import MainAppWindow

class Page:
    pages = []
    current_page = None

    def __init__(self):
        if MainAppWindow.main_frame == None:
            ErrorCodes.PrintErrorWithCode(1003)
            return

        self.page = gui.CreateFrame(MainAppWindow.main_frame)
        gui.SetCurrentFrame(self.page)
        self.OnStart()
        Page.pages.append(self.page)
        gui.ClearCurrentFrame()

    def OnStart(self):
        pass

    def OnExit(self):
        pass

    def PageGrid(self, rows=1, cols=1):
        gui.CreateGrid(self.page, rows=rows, cols=cols)

    def SwitchPages(self, page:int=0):
        if len(Page.pages) < 1:
            ErrorCodes.PrintErrorWithCode(1002)
            return
        
        if page > len(Page.pages) - 1:
            ErrorCodes.PrintErrorWithCode(1003)
            return
        
        if Page.current_page != None:
            Page.current_page.pack_forget()
        
        self.OnExit()
        Page.current_page = Page.pages[page]
        Page.current_page.pack(fill='both', expand=True)
