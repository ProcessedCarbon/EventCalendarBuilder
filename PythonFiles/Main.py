
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from Managers.GUIInterface import GUIInterface
from TextProcessing import TextProcessingManager
from Managers.CalendarInterface import CalendarInterface
from screeninfo import get_monitors

gui = GUIInterface()
ner_Interface = NERInterface()
text_processing = TextProcessingManager()
calendar_interface = CalendarInterface()
#google_Interface = GoogleCalendarInterface()

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

# def CreateGoogleCalendarEvent(event_list:list[dict]):
#     google_events = []
#     for e in event_list:
#         n_event = google_Interface.CreateGoogleEvent(event=str(e["EVENT"]), 
#                                                 location=str(e["LOC"]), 
#                                                 time=e["TIME"][0], 
#                                                 date=e["DATE"],
#                                                 )
#         #print("Event")
#         #print(n_event)
#         google_events.append(n_event)
    
#     if len(google_events) > 0:
#         for g_event in google_events:
#             google_Interface.CreateCalendarEvent(googleEvent=g_event)
#     else:
#         print("NO GOOGLE EVENTS IN LIST")

def CheckText(text):
    t = gui.RetrieveCurrentInputFromText(text)
    t.strip("\n").strip()
    events = ner_Interface.GetEntitiesFromText(text=t)
    ner_Interface.PrintEvents(events)
    print("------------------------------------------------------------------------------")
    print("Process events.....")
    events = ner_Interface.ProcessEvents(events)
    ner_Interface.PrintEvents(events)
    print("------------------------------------------------------------------------------")
    print("Processing text...... ")
    for i in range(len(events)):
        date = events[i]["DATE"]
        events[i]["DATE"] = text_processing.ProcessDateToICSFormat(date=str(date))

        time = events[i]["TIME"]        
        events[i]["TIME"] = text_processing.ProcessTimeToICSFormat(time=str(time))
    ner_Interface.PrintEvents(events)
    print("------------------------------------------------------------------------------")
    print("Generating ICS File")
    print("------------------------------------------------------------------------------")
    print("Done!")

def InitMainGUI(monitor_info):
    monitor_width = int(monitor_info["width"])
    monitor_height = int(monitor_info["height"])
    gui.CreateAppScreen(screen_width=monitor_width, screen_height=monitor_height)

    # Title
    gui.CreateLabel(text="Event Calendar Builder")

    # Text box
    textBox = gui.CreateText(w=150, h=50)

    # Button
    gui.CreateButton(on_click=lambda:CheckText(textBox))

    gui.MainLoop()

monitor_info = GetCurrentMonitorInfo()

if len(monitor_info) > 0:
    InitMainGUI(monitor_info=monitor_info)
else:
    print("No monitor detected!")