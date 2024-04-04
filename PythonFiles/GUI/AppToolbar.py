import logging
from tkinter import messagebox

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import APP_TOOLBAR_GAP_X, APP_TOOLBAR_GAP_Y, SUCCESS_TITLE, HAS_GOOGLE_CONNECTION_MSG, FAILED_TITLE, NO_GOOGLE_CONNECTION_MSG, HAS_OUTLOOK_CONNECTION_MSG, NO_OUTLOOK_CONNECTION_MSG
from Pages.PageManager import PageManager
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface

class AppToolbar:
    def __init__(self) -> None:
        self.events_toolbar_frame = GUIInterface.CreateScrollableFrame(GUIInterface.root, 
                                                                        corner_radius=0,
                                                                        fg_color=GUIInterface.color_palette['CTkProgressBar']['fg_color'])
        
        GUIInterface.CreateGrid(self.events_toolbar_frame, rows=[1,1,1,1,1,1,1,1,1], cols=[1])

        tmp = GUIInterface.current_frame
        GUIInterface.current_frame = self.events_toolbar_frame
    
        # Change page button
        self.logo_label = GUIInterface.CreateLabel(text="Event Calendar Builder", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        self.goToSchedulePageBtn = GUIInterface.CreateButton(text='Schedule Events', on_click=lambda:self.ChangeToPage(0))
        self.goToManageEventsBtn = GUIInterface.CreateButton(text='Manage Events', on_click=lambda:self.ChangeToPage(2))

        # Change Apperance UI
        self.appearance_mode_label = GUIInterface.CreateLabel(text="Appearance Mode:", anchor="w")
        self.appearance_mode_optionemenu = GUIInterface.CreateOptionMenu(values=["Light", "Dark", "System"], command=GUIInterface.SetAppearanceMode)
        self.appearance_mode_optionemenu.set('System')

        # UI Scaling
        self.scaling_label = GUIInterface.CreateLabel(text="UI Scaling:", anchor="w")
        self.scaling_optionemenu = GUIInterface.CreateOptionMenu(values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=GUIInterface.ChangeGUIScaling)
        self.scaling_optionemenu.set('100%')

        # AuthButtons
        self.authGoogleBtn = GUIInterface.CreateButton(text="Authenticate Google Calendar", on_click=self.AuthGoogle)
        self.authOutlookBtn = GUIInterface.CreateButton(text="Authenticate Outlook Calendar", on_click=self.AuthOutlook)

        # GUI Grid
        self.events_toolbar_frame.grid(row=0, column=0, sticky='nswe')
        self.logo_label.grid(row=0, column=0, padx=APP_TOOLBAR_GAP_X, pady=(20, APP_TOOLBAR_GAP_Y))
        self.goToSchedulePageBtn.grid(row=1, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.goToManageEventsBtn.grid(row=2, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.authGoogleBtn.grid(row=3, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.authOutlookBtn.grid(row=4, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.appearance_mode_label.grid(row=5, column=0, padx=APP_TOOLBAR_GAP_X, pady=(APP_TOOLBAR_GAP_Y, 0))
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.scaling_label.grid(row=7, column=0, padx=APP_TOOLBAR_GAP_X, pady=(APP_TOOLBAR_GAP_Y, 0))
        self.scaling_optionemenu.grid(row=8, column=0, padx=APP_TOOLBAR_GAP_X, pady=(APP_TOOLBAR_GAP_Y, 20))

        GUIInterface.current_frame = tmp

    def ChangeToPage(self, page:int)->bool:
        n = len(PageManager.pages)
        if n == 0:
            logging.error(f"[{__name__}] NO PAGES AVAILABLE!")
            return False

        if page > n:
            logging.error(f"[{__name__}] PAGE DOES NOT EXISTS!")
            return False
        
        PageManager.SwitchPages(page)
        return True
    
    def AuthGoogle(self):
        success = GoogleCalendarInterface.ConnectToGoogleCalendar()
        if success:
            messagebox.showinfo(title=SUCCESS_TITLE, message=HAS_GOOGLE_CONNECTION_MSG)
            self.authGoogleBtn.configure(state='disabled')
        else:
            messagebox.showinfo(title=FAILED_TITLE, message=NO_GOOGLE_CONNECTION_MSG)
    
    def AuthOutlook(self):
        outlook_interface.start_flask()
        outlook_interface.auth_event.wait()
        if outlook_interface.auth:
            messagebox.showinfo(title=SUCCESS_TITLE, message=HAS_OUTLOOK_CONNECTION_MSG)
            self.authOutlookBtn.configure(state='disabled')
        else:
            messagebox.showinfo(title=SUCCESS_TITLE, message=NO_OUTLOOK_CONNECTION_MSG)