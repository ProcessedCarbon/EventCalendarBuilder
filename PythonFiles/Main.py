from GUI.GUIInterface import GUIInterface
from GUI.MainAppWindow import MainAppWindow
from Pages.MainPage import MainPage
from Pages.SchedulePage import SchedulePage
from Pages.Page import Page

gui = GUIInterface()

MainAppWindow.Setup()

# Pages
main_page = MainPage()
schedule_page = SchedulePage()

Page.current_page = Page.pages[0]
main_page.SwitchPages(0)

gui.MainLoop()    

