
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from Managers.GUIInterface import GUIInterface
from TextProcessing import TextProcessingManager
from screeninfo import get_monitors

gui = GUIInterface()
ner_Interface = NERInterface()
text_processing = TextProcessingManager()
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
    print("Processing text...... ")
    for event_obj in events:
        for d in event_obj["DATE"]:
            i = event_obj["DATE"].index(d)
            ics_date = text_processing.ProcessDateToICSFormat(date=str(d))
            event_obj["DATE"][i] = ics_date
        
        for t in event_obj["TIME"]:
            i = event_obj["TIME"].index(t)
            ics_time = text_processing.ProcessTimeToICSFormat(time=str(t))
            event_obj["TIME"][i] = ics_time
    print("------------------------------------------------------------------------------")
    print(events)
    print("------------------------------------------------------------------------------")
    print("Done!")

monitor_info = GetCurrentMonitorInfo()

# Initialzation
monitor_width = int(monitor_info["width"])
monitor_height = int(monitor_info["height"])
gui.CreateAppScreen(screen_width=monitor_width, screen_height=monitor_height)

pages = []
current_page = None

def SwitchPages(page:int=0):
    global current_page
    if current_page != None:
        current_page.pack_forget()
    current_page = pages[page]
    current_page.pack()

# PAGES
def MainPage():
    main_page = gui.CreateFrame(gui.main_frame)
    gui.SetCurrentFrame(main_page)
    # Title
    gui.CreateLabel(text="Event Calendar Builder", font_type='Bold', font_size=20)
    # Text box
    gui.CreateText(w=150, h=50)
    # Button
    gui.CreateButton(on_click=lambda:SwitchPages(1))

    pages.append(main_page)

def SchedulePromptPage():
    schedule_page = gui.CreateFrame(gui.main_frame)
    gui.SetCurrentFrame(schedule_page)

    # Title
    gui.CreateLabel(text="Schedule Page")
    # Text box
    gui.CreateText(w=50, h=50)

    pages.append(schedule_page)

# Stored in pages in order
MainPage()
SchedulePromptPage()

SwitchPages()

gui.MainLoop()
    