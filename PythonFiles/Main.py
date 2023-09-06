
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from Managers.GUIInterface import GUIInterface
from TextProcessing import TextProcessingManager
from screeninfo import get_monitors

gui = GUIInterface()
ner_Interface = NERInterface()
text_processing = TextProcessingManager()
google_Interface = GoogleCalendarInterface()

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

def CreateGoogleCalendarEvent(event_list:list[dict]):
    google_events = []
    for e in event_list:
        n_event = google_Interface.CreateGoogleEvent(event=str(e["EVENT"]), 
                                                location=str(e["LOC"]), 
                                                time=e["TIME"][0], 
                                                date=e["DATE"],
                                                )
        #print("Event")
        #print(n_event)
        google_events.append(n_event)
    
    if len(google_events) > 0:
        for g_event in google_events:
            google_Interface.CreateCalendarEvent(googleEvent=g_event)
    else:
        print("NO GOOGLE EVENTS IN LIST")

def CheckText(text):
    t = gui.RetrieveCurrentInputFromText(text)
    t.strip("\n").strip()
    events = ner_Interface.GetEntitiesFromText(text=t)
    ner_Interface.PrintEvents(events)
    print("------------------------------------------------------------------------------")
    print("Processing text to google format ...... ")
    for event_obj in events:
        for d in event_obj["DATE"]:
            i = event_obj["DATE"].index(d)
            g_date = text_processing.ProcessDateForGoogleCalendar(date_text=str(d))
            event_obj["DATE"][i] = g_date
        
        for t in event_obj["TIME"]:
            i = event_obj["TIME"].index(t)
            g_time = text_processing.ProcessTimeForGoogleCalendars(time_text=str(t))
            event_obj["TIME"][i] = g_time
    print("------------------------------------------------------------------------------")
    ner_Interface.PrintEvents(events)
    print("------------------------------------------------------------------------------")
    print("Creating calendar event ......")
    CreateGoogleCalendarEvent(events)
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