import logging

from GUI.GUIInterface import GUIInterface
from GUI.GUIConstants import APP_TOOLBAR_GAP_X, APP_TOOLBAR_GAP_Y
from Pages.PageManager import PageManager

class AppToolbar:
    def __init__(self) -> None:
        self.events_toolbar_frame = GUIInterface.CreateScrollableFrame(GUIInterface.root, 
                                                                        corner_radius=0,
                                                                        fg_color=GUIInterface.color_palette['CTkProgressBar']['fg_color'])
        
        GUIInterface.CreateGrid(self.events_toolbar_frame, rows=[1,1,1,1,1,1,1], cols=[1])

        tmp = GUIInterface.current_frame
        GUIInterface.current_frame = self.events_toolbar_frame
    
        # Change page button
        self.logo_label = GUIInterface.CreateLabel(text="Event Calendar Builder", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        self.sidebar_button_1 = GUIInterface.CreateButton(text='Schedule Events', on_click=lambda:self.ChangeToPage(0))
        self.sidebar_button_2 = GUIInterface.CreateButton(text='Manage Events', on_click=lambda:self.ChangeToPage(2))

        # Change Apperance UI
        self.appearance_mode_label = GUIInterface.CreateLabel(text="Appearance Mode:", anchor="w")
        self.appearance_mode_optionemenu = GUIInterface.CreateOptionMenu(values=["Light", "Dark", "System"], command=GUIInterface.SetAppearanceMode)
        self.appearance_mode_optionemenu.set('System')

        # UI Scaling
        self.scaling_label = GUIInterface.CreateLabel(text="UI Scaling:", anchor="w")
        self.scaling_optionemenu = GUIInterface.CreateOptionMenu(values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=GUIInterface.ChangeGUIScaling)
        self.scaling_optionemenu.set('100%')

        # GUI Grid
        self.events_toolbar_frame.grid(row=0, column=0, sticky='nswe')
        self.logo_label.grid(row=0, column=0, padx=APP_TOOLBAR_GAP_X, pady=(20, APP_TOOLBAR_GAP_Y))
        self.sidebar_button_1.grid(row=1, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.sidebar_button_2.grid(row=2, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.appearance_mode_label.grid(row=3, column=0, padx=APP_TOOLBAR_GAP_X, pady=(APP_TOOLBAR_GAP_Y, 0))
        self.appearance_mode_optionemenu.grid(row=4, column=0, padx=APP_TOOLBAR_GAP_X, pady=APP_TOOLBAR_GAP_Y)
        self.scaling_label.grid(row=5, column=0, padx=APP_TOOLBAR_GAP_X, pady=(APP_TOOLBAR_GAP_Y, 0))
        self.scaling_optionemenu.grid(row=6, column=0, padx=APP_TOOLBAR_GAP_X, pady=(APP_TOOLBAR_GAP_Y, 20))

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