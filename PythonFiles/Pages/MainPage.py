from tkinter import messagebox
import logging
from customtkinter import filedialog
import os    

from Pages.Page import PageManager, Page
from NER.NERInterface import NERInterface
from GUI.MainAppWindow import MainAppWindow
from Events.EventsManager import EventsManager
from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import TEXT_BOX_MODIFIER, FAILED_TITLE, SUCCESS_TITLE
import Managers.DirectoryManager as dir_manager

class MainPage(Page):
        def __init__(self): 
                self.main_page_textbox = None
                super().__init__()

        def OnStart(self):
                rows = [1,1,1]
                cols = [1,10,1]
                self.PageGrid(rows=rows, cols=cols)

                # Text box
                self.main_page_textbox = GUIInterface.CreateTextbox(width=MainAppWindow.app_width * TEXT_BOX_MODIFIER, height=MainAppWindow.app_height * TEXT_BOX_MODIFIER)

                tmp = GUIInterface.current_frame
                self.button_frame = GUIInterface.CreateFrame(GUIInterface.current_frame, 
                                                                fg_color=self.page_color,
                                                                border_color=self.page_color)

                self.button_frame.columnconfigure(0, weight=1)
                self.button_frame.columnconfigure(1, weight=1)
                self.button_frame.columnconfigure(2, weight=1)
                self.button_frame.rowconfigure(0, weight=1)
                self.button_frame.rowconfigure(1, weight=1)
                self.button_frame.rowconfigure(2, weight=1)

                # Buttons
                self.submit_button = GUIInterface.CreateButton(text="Submit Text", on_click=lambda:self.Submit(self.main_page_textbox))
                self.upload_file_btn = GUIInterface.CreateButton(text='Upload File To Read Text', on_click=self.OnUpload)

                # Grid GUI
                self.main_page_textbox.grid(row=1, column=1, sticky='nsew')
                self.button_frame.grid(row=2, column=1, sticky='nsew')
                self.submit_button.grid(row=1, column=0)
                self.upload_file_btn.grid(row=1, column=2)

                GUIInterface.current_frame = tmp
        
        def OnEntry(self):
                self.main_page_textbox.focus_set() # sets keyboard events to this textbox

        def OnExit(self):
                if self.main_page_textbox != None:
                        GUIInterface.ClearTextBox(self.main_page_textbox)
                        return
                logging.warning(f"[{__name__}] MISSING TEXTBOX REFERENCE")

        def Submit(self, textbox):
                self.ReadAndProcessText(textbox)
                PageManager.SwitchPages(1) 

        def ReadAndProcessText(self,textbox)->bool:
                t = GUIInterface.RetrieveCurrentInputFromTextbox(textbox)

                if t == "" or t == " " or t == "\n":
                        return

                t.strip("\n").strip()
                events = NERInterface.GetEntitiesFromText(text=t)
                p_events = EventsManager.ProcessEvents(events)
                EventsManager.AddEvents(events=p_events)
                return
        
        def OnUpload(self):
                file_path = filedialog.askopenfilename(filetypes=[("EML Files", "*.eml"), ("Text Files", ".txt")])
                if file_path:
                        _, file_extension = os.path.splitext(file_path)
                        try:
                                GUIInterface.ClearTextBox(self.main_page_textbox)
                                if file_extension.lower() == ".eml":
                                        content, subject, sender, recipients, date = dir_manager.ReadEMLFile(file_path)
                                else:
                                        content = dir_manager.FileRead(file_path)
                                GUIInterface.UpdateTextBox(textbox=self.main_page_textbox, state='normal', text=content)
                                messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully read file')
                        except Exception as e:
                                messagebox.showinfo(title=FAILED_TITLE, message=f'Failed to read file due to {e}')
                                logging.error(f'[{__name__}] FAILED TO READ FILE DUE TO {e}')
