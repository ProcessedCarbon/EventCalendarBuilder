from Managers.DirectoryManager import DirectoryManager
DirectoryManager()

from GUI.GUIInterface import GUIInterface
from GUI.MainAppWindow import MainAppWindow
from Pages.MainPage import MainPage
from Pages.SchedulePage import SchedulePage
from Pages.PageManager import PageManager

gui = GUIInterface()

MainAppWindow.Setup()

# Pages
main_page = MainPage()
schedule_page = SchedulePage()

PageManager.SwitchPages(0)

gui.MainLoop()    

