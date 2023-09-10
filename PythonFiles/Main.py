from GUI.GUIInterface import GUIInterface
from GUI.MainAppWindow import MainAppWindow
from GUI.MainPage import MainPage
from GUI.SchedulePage import SchedulePage
from GUI.Page import Page

gui = GUIInterface()

MainAppWindow.Setup()

# Pages
main_page = MainPage()
schedule_page = SchedulePage()

Page.current_page = Page.pages[0]
main_page.SwitchPages(0)

gui.MainLoop()    

