from GUI.GUIInterface import GUIInterface
from GUI.MainAppWindow import MainAppWindow
from GUI.MainPage import MainPage
from GUI.SchedulePage import SchedulePage

gui = GUIInterface()

MainAppWindow.Setup()

# Pages
schedule_page = SchedulePage()
main_page = MainPage()

gui.MainLoop()    

