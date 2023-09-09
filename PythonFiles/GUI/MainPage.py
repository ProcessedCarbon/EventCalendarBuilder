from GUI.Page import Page
from GUI.GUIInterface import GUIInterface as gui
from NERInterface import NERInterface
from TextProcessing import TextProcessingManager
from GUI.MainAppWindow import MainAppWindow

class MainPage(Page):
    events = []

    def __init__(self): 
        super().__init__()
    
    def OnStart(self):
        self.PageGrid(rows=3, cols=3)
                
        # Title
        title = gui.CreateLabel(text="Event Calendar Builder", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n', pady=10)

        # Text box
        textbox = gui.CreateText(w=MainAppWindow.app_width * 0.5, h=MainAppWindow.app_height * 0.5)
        textbox.grid(row=1, column=1, sticky='nsew')

        # Button
        button = gui.CreateButton(text="Submit", on_click=lambda:self.CheckText(textbox))
        button.grid(row=2, column=1, stick='s', pady=10)
    
    def CheckText(self,textbox):
        t = gui.RetrieveCurrentInputFromTextbox(textbox)

        if t == "" or t == " ":
            print("Empty text")
            return
        
        t.strip("\n").strip()
        MainPage.events = NERInterface.GetEntitiesFromText(text=t)
        print("------------------------------------------------------------------------------")
        print("Process events.....")
        MainPage.events = NERInterface.ProcessEvents(MainPage.events)
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
        self.SwitchPages(1)