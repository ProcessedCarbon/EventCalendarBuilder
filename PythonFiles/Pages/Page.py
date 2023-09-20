from GUI.GUIInterface import GUIInterface
from Managers.ErrorConfig import ErrorCodes
from Pages.PageManager import PageManager

class Page:
    def __init__(self):
        if GUIInterface.root == None:
            ErrorCodes.PrintErrorWithCode(1003)
            return

        self.page = GUIInterface.CreateFrame(GUIInterface.root)
        self.page.grid(row=0, column=0, sticky="nsew")
        PageManager.AddPage(self)
    
        self.OnStart()
        GUIInterface.ClearCurrentFrame()

    def OnStart(self):
        pass

    def OnEntry(self):
        pass

    def OnExit(self):
        pass

    def PageGrid(self, rows=list[int], cols=list[int]):
        GUIInterface.CreateGrid(self.page, rows=rows, cols=cols)
    
    def SwitchTo(self):
        self.page.tkraise()
    
    def Prompt(self, promt_str:str):
        print("Prompt: " + promt_str.upper() + "!")