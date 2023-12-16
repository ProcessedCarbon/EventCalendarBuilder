import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

'''
MANAGERS AND INTERFACES
'''
from GUI.GUIInterface import GUIInterface
from Pages.PageManager import PageManager
from Calendar.GoogleCalendar.GoogleCalendarInterface import GoogleCalendarInterface
import Calendar.Outlook.OutlookInterface as outlook_interface
import Managers.MultiprocessingManager as multiprocessing_manager

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

def client_app():
    gui = GUIInterface()
    GUIInterface.SetDefaultColorTheme('Oceanix.json')

    # Application initilization
    MainAppWindow.Setup()
    EventsManager.UpdateEventsDB() # Initialize local event db

    # Page initilialization
    MainPage()                 
    SchedulePage()          
    ManageEventPage()   
    PageManager.SwitchPages(0)

    # Toolbar
    AppToolbar() # Must be called here after all pages are created as it requires a list[Page] of all pages
    gui.MainLoop()

if __name__ == "__main__":
    #GoogleCalendarInterface.ConnectToGoogleCalendar()
    #multiprocessing_manager.add_process('OUTLOOK', outlook_interface.run)
    #processes = multiprocessing_manager.process_dict
    #processes['OUTLOOK'].start()
    client_app()
