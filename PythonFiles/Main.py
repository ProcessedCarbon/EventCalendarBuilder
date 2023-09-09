from GUI.GUIInterface import GUIInterface

from GUI.MainAppWindow import MainAppWindow
from GUI.Page import Page
from GUI.MainPage import MainPage
from GUI.SchedulePage import SchedulePage

gui = GUIInterface()

# Initialzation

events = []
list_of_globals = globals()

MainAppWindow.Setup()
main_page = MainPage()
schedule_page = SchedulePage()

Page.current_page = Page.pages[0]
Page.current_page.pack(fill='both', expand=True)

gui.MainLoop()    

