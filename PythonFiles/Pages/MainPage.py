from tkinter import messagebox
import logging
from customtkinter import filedialog    

from Pages.Page import PageManager, Page
from NER.NERInterface import NERInterface
from GUI.MainAppWindow import MainAppWindow
from Events.EventsManager import EventsManager
from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import TEXT_BOX_MODIFIER, WARNING_TITLE, NO_TEXT_FOUND_MSG, FAILED_TITLE, SUCCESS_TITLE
import Managers.DirectoryManager as dir_manager
from Managers.TextProcessing import TextProcessingManager

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
                self.submit_button = GUIInterface.CreateButton(text="Submit", on_click=lambda:self.Submit(self.main_page_textbox))
                self.go_to_schedule_btn = GUIInterface.CreateButton(text='Go To Schedule', on_click=lambda:PageManager.SwitchPages(1))
                self.upload_file_btn = GUIInterface.CreateButton(text='Upload EML File', on_click=self.OnUpload)

                # Grid GUI
                self.main_page_textbox.grid(row=1, column=1, sticky='nsew')
                self.button_frame.grid(row=2, column=1, sticky='nsew')
                self.submit_button.grid(row=1, column=0)
                self.go_to_schedule_btn.grid(row=1, column=1)
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
                success = self.ReadAndProcessText(textbox)
                if success:
                        PageManager.SwitchPages(1) 

        def ReadAndProcessText(self,textbox)->bool:
                t = GUIInterface.RetrieveCurrentInputFromTextbox(textbox)

                if t == "" or t == " " or t == "\n":
                        messagebox.showinfo(title=WARNING_TITLE, message=NO_TEXT_FOUND_MSG)
                        return False

                t.strip("\n").strip()
                events = NERInterface.GetEntitiesFromText(text=t)
                p_events = EventsManager.ProcessEvents(events)
                EventsManager.AddEvents(events=p_events)
                return True
        
        def OnUpload(self):
                eml_file_path = filedialog.askopenfilename(filetypes=[("EML Files", "*.eml")])
                if eml_file_path:
                        try:
                                GUIInterface.ClearTextBox(self.main_page_textbox)
                                content, subject, sender, recipients, date = dir_manager.ReadEMLFile(eml_file_path)
                                GUIInterface.UpdateTextBox(textbox=self.main_page_textbox, state='normal', text=content)
                                messagebox.showinfo(title=SUCCESS_TITLE, message=f'Successfully read .eml file with subject:\n{subject}')
                        except Exception as e:
                                messagebox.showinfo(title=FAILED_TITLE, message=f'Failed to read file due to {e}')
                                logging.error(f'[{__name__}] FAILED TO READ .eml FILE DUE TO {e}')
