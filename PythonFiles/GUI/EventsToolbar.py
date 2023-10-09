from GUI.GUIInterface import GUIInterface
from Managers.ErrorConfig import ErrorCodes
from Pages.PageManager import PageManager

class EventsToolbar:
    def __init__(self) -> None:
        self.events_toolbar_frame = GUIInterface.CreateScrollableFrame(GUIInterface.root, 
                                                                       corner_radius=0,)
        
        self.events_toolbar_frame.grid(row=0, column=0, rowspan=4, sticky='nswe')
        self.events_toolbar_frame.grid_rowconfigure(4, weight=1)

        tmp = GUIInterface.current_frame
        GUIInterface.SetCurrentFrame(self.events_toolbar_frame)

        # Change page button
        self.logo_label = GUIInterface.CreateLabel(text="Event Calendar Builder", font=GUIInterface.getCTKFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = GUIInterface.CreateButton(text='Text Input', on_click=lambda:self.ChangeToPage(0))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = GUIInterface.CreateButton(text='Manage Events', on_click=lambda:self.ChangeToPage(2))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Change Apperance UI
        self.appearance_mode_label = GUIInterface.CreateLabel(text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = GUIInterface.CreateOptionMenu(values=["Light", "Dark", "System"], command=GUIInterface.SetAppearanceMode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        GUIInterface.SetCurrentFrame(tmp)
    
    def ChangeToPage(self, page:int)->bool:
        n = len(PageManager.pages)
        if n == 0:
            ErrorCodes.PrintCustomError("NO PAGES AVAILABLE!")
            return False

        if page > n:
            ErrorCodes.PrintCustomError("PAGE DOES NOT EXISTS!")
            return False
        
        PageManager.SwitchPages(page)
        return True