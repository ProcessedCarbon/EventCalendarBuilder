from Pages.Page import *
from GUI.GUIInterface import GUIInterface as gui
from NER.NERInterface import NERInterface
from Managers.TextProcessing import TextProcessingManager
from GUI.MainAppWindow import MainAppWindow
from Pages.PageManager import PageManager

class MainPage(Page):
    events = []

    def __init__(self): 
        super().__init__()
    
    def OnStart(self):
        rows = [1, 1, 1]
        cols = [1, 1, 1]
        self.PageGrid(rows=rows, cols=cols)
                
        # Title
        title = gui.CreateLabel(text="Event Calendar Builder", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n', pady=10)

        # Text box
        textbox = gui.CreateTextbox(width=MainAppWindow.app_width * 0.5, height=MainAppWindow.app_height * 0.5)
        textbox.grid(row=1, column=1, sticky='nsew')

        # Button
        button = gui.CreateButton(text="Submit", on_click=lambda:self.Submit(textbox))
        button.grid(row=2, column=1, stick='s', pady=10)
    
    def Submit(self, textbox):
        success = self.ReadAndProcessText(textbox)
        
        if success:
            PageManager.SwitchPages(1) 

    def ReadAndProcessText(self,textbox)->bool:
        t = gui.RetrieveCurrentInputFromTextbox(textbox)

        if t == "" or t == " " or t == "\n":
            print("No text found!")
            return False
        
        t.strip("\n").strip()
        MainPage.events = NERInterface.GetEntitiesFromText(text=t)

        # Process time and date using the same events list
        if len(MainPage.events) > 0:
            print("------------------------------------------------------------------------------")
            print("Process events.....")
            MainPage.events = NERInterface.ProcessEvents(MainPage.events)
            NERInterface.PrintEvents(MainPage.events)
            print("------------------------------------------------------------------------------")
            print("Processing text...... ")
            for i in range(len(MainPage.events)):
                date = MainPage.events[i]["DATE"]
                MainPage.events[i]["DATE"] = TextProcessingManager.ProcessDate(date_text=str(date))

                time = MainPage.events[i]["TIME"]        
                MainPage.events[i]["TIME"] = TextProcessingManager.ProcessTime(time_text=str(time))
            NERInterface.PrintEvents(MainPage.events)
            print("------------------------------------------------------------------------------")
            globals()['events'] = MainPage.events
            print("Done!")

        return True
    
    def ClearEvents():
        MainPage.events = []