from GUI.GUIInterface import GUIInterface
from Calendar.CalendarInterface import CalendarInterface
import os, signal
import logging

class MainAppWindow:
    aspect = 0.85
    main_frame = None

    monitor_width = GUIInterface.monitor_width
    monitor_height =  GUIInterface.monitor_height
    app_width = int(monitor_width * aspect)
    app_height = int(monitor_height * aspect)

    def Setup():
        GUIInterface.root.geometry(f'{MainAppWindow.app_width}x{MainAppWindow.app_height}')

        GUIInterface.root.columnconfigure(0, weight=1)
        GUIInterface.root.columnconfigure(1, weight=5)
        GUIInterface.root.rowconfigure(0, weight=1)

        GUIInterface.root.protocol("WM_DELETE_WINDOW", MainAppWindow.OnAppClose) 
        GUIInterface.root.update()

    def OnAppClose():
        logging.info('App Closing')
        logging.info('Removing ICS files')
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)
        GUIInterface.root.destroy()
        # Kill process
        os.kill(os.getpid(), signal.SIGINT)
        logging.info('CLOSED')