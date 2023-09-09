from NERInterface import NERInterface
from GUI.GUIInterface import GUIInterface
from TextProcessing import TextProcessingManager
from Managers.CalendarInterface import CalendarInterface

from GUI.MainAppWindow import MainAppWindow
from GUI.Page import Page
from GUI.MainPage import MainPage
from GUI.SchedulePage import SchedulePage

gui = GUIInterface()
ner = NERInterface()
text_processing = TextProcessingManager()
cal = CalendarInterface()

# Initialzation

events = []
list_of_globals = globals()

MainAppWindow.Setup()
main_page = MainPage()
schedule_page = SchedulePage()

Page.current_page = Page.pages[0]
Page.current_page.pack(fill='both', expand=True)

gui.MainLoop()    

