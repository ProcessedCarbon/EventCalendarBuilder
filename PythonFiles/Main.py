import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

from GUI.GUIInterface import GUIInterface
from GUI.MainAppWindow import MainAppWindow
from Pages.PageManager import PageManager
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface

# Pages
from Pages.MainPage import MainPage
from Pages.SchedulePage import SchedulePage
from Pages.ManageEventPage import ManageEventPage

# Toolbar
from GUI.EventsToolbar import EventsToolbar

import threading

#GoogleCalendarInterface.ConnectToGoogleCalendar()
#outlook_interface.start()
threading.Thread(target=outlook_interface.start).start() # run the Flask app in a thread
gui = GUIInterface()

MainAppWindow.Setup()

main_page = MainPage()                  # 1
schedule_page = SchedulePage()          # 2
maangerevent_page = ManageEventPage()   # 3

PageManager.SwitchPages(0)

# Toolbar
# Must be called here after all pages are created as it requires a list[Page] of all pages
events_toolbar = EventsToolbar()

gui.MainLoop()    

