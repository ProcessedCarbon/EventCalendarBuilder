from Pages.Page import PageManager, Page
from NER.NERInterface import NERInterface
from GUI.MainAppWindow import MainAppWindow
from Events.EventsManager import EventsManager
from GUI.GUIInterface import GUIInterface
import GUI.PopupManager as popup_mgr
import logging

class MainPage(Page):
    def __init__(self): 
        self.main_page_textbox = None
        super().__init__()
    
    def OnStart(self):
        rows = [1,1,1]
        cols = [1,10,1]
        self.PageGrid(rows=rows, cols=cols)

        # Text box
        self.main_page_textbox = GUIInterface.CreateTextbox(width=MainAppWindow.app_width * 0.5, height=MainAppWindow.app_height * 0.5)
        self.main_page_textbox.grid(row=1, column=1, sticky='nsew')

        tmp = GUIInterface.current_frame
        self.button_frame = GUIInterface.CreateFrame(GUIInterface.current_frame, 
                                                     fg_color=self.page_color,
                                                     border_color=self.page_color)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        self.button_frame.rowconfigure(2, weight=1)
        self.button_frame.grid(row=2, column=1, sticky='nsew')

        # Button
        button = GUIInterface.CreateButton(text="Submit", on_click=lambda:self.Submit(self.main_page_textbox))
        button.grid(row=1, column=0)

        # Go to schedule
        go_to_schedule_btn = GUIInterface.CreateButton(text='To Schedule', on_click=lambda:PageManager.SwitchPages(1))
        go_to_schedule_btn.grid(row=1, column=1)

        GUIInterface.current_frame = tmp

    def OnExit(self):
        if self.main_page_textbox != None:
            GUIInterface.ClearTextBox(self.main_page_textbox)
            return
        #print(f"[{__name__}] MISSING TEXTBOX REFERENCE")
        logging.warning(f"[{__name__}] MISSING TEXTBOX REFERENCE")

    def Submit(self, textbox):
        success = self.ReadAndProcessText(textbox)
        
        if success:
            PageManager.SwitchPages(1) 

    def ReadAndProcessText(self,textbox)->bool:
        t = GUIInterface.RetrieveCurrentInputFromTextbox(textbox)

        if t == "" or t == " " or t == "\n":
            #print("No text found!")
            popup_mgr.BasicPopup('No text found!\nPlease input text')
            return False
        
        t.strip("\n").strip()
        events = NERInterface.GetEntitiesFromText(text=t)

        # Process time and date using the same events list
        #print("Process Events")
        p_events = EventsManager.ProcessEvents(events)
        #for e in p_events: print(e)

        #print("------------------------------------------------------------------------------")
        #print("Process and Add to event manager list")
        added_events = EventsManager.AddEvents(events=p_events)
        #for e in added_events: print(e)
        #print("------------------------------------------------------------------------------")            
        #print("Done!")
        return True