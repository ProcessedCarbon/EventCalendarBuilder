
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
    current_page.pack(fill='both', expand=True)

# PAGES
def MainPage():
    main_page = gui.CreateFrame(frame_target=gui.main_frame)
    gui.SetCurrentFrame(main_page)
    
    # Title
    title = gui.CreateLabel(text="Event Calendar Builder", font=("Bold",20))
    title.pack()

    # Text box
    textbox = gui.CreateText(w=150, h=50)
    textbox.pack()

    # Button
    button = gui.CreateButton(text="Submit", on_click=lambda:SwitchPages(1))
    button.pack()

    pages.append(main_page)
    gui.ClearCurrentFrame()

def SchedulePromptPage():
    #Schedule Page Params
    columns = 3

    # GUI
    schedule_page = gui.CreateFrame(gui.main_frame)
    gui.SetCurrentFrame(schedule_page)

    for i in range(columns):
        schedule_page.columnconfigure(i, weight=1)
        schedule_page.rowconfigure(i, weight=1)

    # Back Button
    button = gui.CreateButton(text="<", on_click=lambda:SwitchPages(0))
    button.grid(row=0, column=0, sticky='nw')

    # Title
    title = gui.CreateLabel(text="Schedule", font=("Bold",20))
    title.grid(row=0, column=1, sticky='n')

    details_frame = gui.CreateFrame(schedule_page)
    num_details = 6
    for i in range(num_details):
        details_frame.rowconfigure(i, weight=1)
    details_frame.grid(row=1, column=1, sticky='nsew')

    # Details entry
    paddint_y = 10
    gui.CreateEntryWithLabel(frame_target=details_frame, label="Event:", frame_row=0, pady=paddint_y)
    gui.CreateEntryWithLabel(frame_target=details_frame, label="Description:", frame_row=1, pady=paddint_y)
    gui.CreateEntryWithLabel(frame_target=details_frame, label="Priority:", frame_row=2, pady=paddint_y)
    gui.CreateEntryWithLabel(frame_target=details_frame, label="Location:", frame_row=3, pady=paddint_y)
    gui.CreateEntryWithLabel(frame_target=details_frame, label="Start Datetime:", frame_row=4, pady=paddint_y)
    gui.CreateEntryWithLabel(frame_target=details_frame, label="End Datetime:", frame_row=5, pady=paddint_y)

    pages.append(schedule_page)
    gui.ClearCurrentFrame()

# Stored in pages in order
MainPage()
SchedulePromptPage()

SwitchPages(1)

gui.MainLoop()    