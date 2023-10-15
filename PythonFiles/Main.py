import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

'''
MANAGERS AND INTERFACES
'''
from GUI.GUIInterface import GUIInterface
from Pages.PageManager import PageManager
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface

from Events.EventsManager import EventsManager

'''
GUI
'''
# Windows
from GUI.MainAppWindow import MainAppWindow

# Pages
from Pages.MainPage import MainPage
from Pages.SchedulePage import SchedulePage
from Pages.ManageEventPage import ManageEventPage

# Toolbar
from GUI.AppToolbar import AppToolbar

#GoogleCalendarInterface.ConnectToGoogleCalendar()
gui = GUIInterface()

# Application initilization
MainAppWindow.Setup()
EventsManager.UpdateEventsDB() # Initialize local event db

# Page initilialization
main_page = MainPage()                  # 1
schedule_page = SchedulePage()          # 2
manage_event_page = ManageEventPage()   # 3
PageManager.SwitchPages(0)

# Toolbar
toolbar = AppToolbar() # Must be called here after all pages are created as it requires a list[Page] of all pages

gui.MainLoop()    

