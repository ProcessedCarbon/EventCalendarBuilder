from Pages.Page import *
from NER.NERInterface import NERInterface
from Managers.TextProcessing import TextProcessingManager
from GUI.MainAppWindow import MainAppWindow

class MainPage(Page):
    def __init__(self): 
        super().__init__()
    
    def OnStart(self):
        rows = [1, 1, 1]
        cols = [1, 1, 1]
        self.PageGrid(rows=rows, cols=cols)
                
        # Title
        title = GUIInterface.CreateLabel(text="Event Calendar Builder", font=("Bold",20))
        title.grid(row=0, column=1, sticky='n', pady=10)

        # Text box
        textbox = GUIInterface.CreateTextbox(width=MainAppWindow.app_width * 0.5, height=MainAppWindow.app_height * 0.5)
        textbox.grid(row=1, column=1, sticky='nsew')

        # Button
        button = GUIInterface.CreateButton(text="Submit", on_click=lambda:self.Submit(textbox))
        button.grid(row=2, column=1, stick='s', pady=10)
    
    def Submit(self, textbox):
        success = self.ReadAndProcessText(textbox)
        
        if success:
            PageManager.SwitchPages(1) 

    def ReadAndProcessText(self,textbox)->bool:
        t = GUIInterface.RetrieveCurrentInputFromTextbox(textbox)

        if t == "" or t == " " or t == "\n":
            print("No text found!")
            return False
        
        t.strip("\n").strip()
        NERInterface.events = NERInterface.GetEntitiesFromText(text=t)

        # Process time and date using the same events list
        if len(NERInterface.events) > 0:
            print("------------------------------------------------------------------------------")
            print("Process events.....")
            NERInterface.events = NERInterface.ProcessEvents(NERInterface.events)
            NERInterface.PrintEvents(NERInterface.events)
            print("------------------------------------------------------------------------------")
            print("Processing text...... ")
            for i in range(len(NERInterface.events)):
                date = NERInterface.events[i]["DATE"]
                NERInterface.events[i]["DATE"] = TextProcessingManager.ProcessDate(date_text=str(date))

                time = NERInterface.events[i]["TIME"]        
                NERInterface.events[i]["TIME"] = TextProcessingManager.ProcessTime(time_text=str(time))
            NERInterface.PrintEvents(NERInterface.events)
            print("------------------------------------------------------------------------------")
            print("Done!")

        return True