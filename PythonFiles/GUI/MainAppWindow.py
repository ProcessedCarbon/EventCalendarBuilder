from screeninfo import get_monitors
from GUI.GUIInterface import GUIInterface
import Managers.MultiprocessingManager as multiprocessing_mgr
from Calendar.CalendarInterface import CalendarInterface

def GetCurrentMonitorInfo()->dict:
        # Monitor(x=0, y=0, width=3840, height=2160, width_mm=708, height_mm=399, name='DP-0', is_primary=True)
        current = {}
        for m in get_monitors():
            s = str(m)
            # Had to do this way cause splitting with brackets as pattern causes issues
            s = s.replace("Monitor","").replace("(", "").replace(")", "").replace(" ","")
            split = s.split(",")

            is_primary_split = split[len(split) - 1].split("=")
            is_primary = bool(is_primary_split[1])
            if is_primary == False:
                continue

            for i in range(len(split)):
                var_split = split[i].split("=")
                current[var_split[0]] = var_split[1]

        return current 

class MainAppWindow:
    aspect = 0.8
    main_frame = None

    monitor_info = GetCurrentMonitorInfo()
    monitor_width = int(monitor_info["width"])
    monitor_height = int(monitor_info["height"])
    app_width = int(monitor_width * aspect)
    app_height = int(monitor_height * aspect)

    def Setup():
        GUIInterface.root.geometry(f'{MainAppWindow.app_width}x{MainAppWindow.app_height}')

        GUIInterface.root.columnconfigure(0, weight=1)
        GUIInterface.root.columnconfigure(1, weight=5)
        GUIInterface.root.rowconfigure(0, weight=1)

        GUIInterface.root.protocol("WM_DELETE_WINDOW", MainAppWindow.OnAppClose) 

    def OnAppClose():
        processes = multiprocessing_mgr.processes
        print('App Closing')
        print(f'Num processes: {len(processes)}')
        print('Terminating processes')
        for p in processes:
            p.terminate()
            p.join()
        print('Removing ICS files')
        CalendarInterface.DeleteICSFilesInDir(CalendarInterface._main_dir)
        GUIInterface.root.destroy()
    


