import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

from GUI.GUIInterface import GUIInterface
from GUI.MainAppWindow import MainAppWindow
from Pages.MainPage import MainPage
from Pages.SchedulePage import SchedulePage
from Pages.PageManager import PageManager
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface

#GoogleCalendarInterface.ConnectToGoogleCalendar()
gui = GUIInterface()

MainAppWindow.Setup()

# Pages
main_page = MainPage()
schedule_page = SchedulePage()

PageManager.SwitchPages(0)

gui.MainLoop()    

