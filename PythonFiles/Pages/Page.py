import logging

from GUI.GUIInterface import GUIInterface
from Pages.PageManager import PageManager

class Page:
    def __init__(self):
        if GUIInterface.root == None:
            #print(f"[{__name__}] MISSING PAGES, PAGE NOT FOUND!")
            logging.error(f"[{__name__}] MISSING PAGES, PAGE NOT FOUND!")
            return

        self.page_color = tuple(GUIInterface.color_palette['CTkFrame']['fg_color'])
        self.page = GUIInterface.CreateFrame(GUIInterface.root,
                                            fg_color=self.page_color)
        self.page.grid(row=0, column=1, sticky="nsew")
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