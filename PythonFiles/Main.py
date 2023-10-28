import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

'''
MANAGERS AND INTERFACES
'''
from GUI.GUIInterface import GUIInterface
from Pages.PageManager import PageManager
from GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface

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

from multiprocessing import Process, Queue

#GoogleCalendarInterface.ConnectToGoogleCalendar()
def client_app(processes):
    gui = GUIInterface()

    # Application initilization
    MainAppWindow.Setup(processes)
    EventsManager.UpdateEventsDB() # Initialize local event db

    # Page initilialization
    MainPage()                  # 1
    SchedulePage()          # 2
    ManageEventPage()   # 3
    PageManager.SwitchPages(0)

    # Toolbar
    AppToolbar() # Must be called here after all pages are created as it requires a list[Page] of all pages

    gui.MainLoop()

if __name__ == "__main__":
    q = Queue()
    processes = []

    flask_process = Process(target=outlook_interface.run)
    google_process = Process(target=GoogleCalendarInterface.ConnectToGoogleCalendar)

    processes.append(google_process)
    processes.append(flask_process)

    for p in processes:
        p.start()
        q.put(p)
        
    client_app(processes)

    for p in processes: p.join()
    
        
