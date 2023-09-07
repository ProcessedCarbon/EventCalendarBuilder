
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from TextProcessing import TextProcessingManager

# Extracts text from plain text file 
def getTestingText(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.read()
    
    return lines

# Test case for single event w/ its corresponding details
def SingleEventTest():
    print("------------------------------------------------------------------------------")
    print("Reading testing text in progress....")
    testing_file_path = "./Testing/testing_text_single.txt"
    test_text = getTestingText(file_path=testing_file_path)
    print(test_text)
    print("------------------------------------------------------------------------------")
    print("Reading Done!")

    print("------------------------------------------------------------------------------")
    print("Getting Entities from text.....")
    ner_Interface = NERInterface()
    events = ner_Interface.GetEntitiesFromText(text=test_text)
    
    ner_Interface.PrintEvents(events)

    print("------------------------------------------------------------------------------")
    print("Processing text to google format ...... ")
    text_processing = TextProcessingManager()

    for event_obj in events:
        for d in event_obj["DATE"]:
            i = event_obj["DATE"].index(d)
            g_date = text_processing.ProcessDate(date_text=str(d))
            event_obj["DATE"][i] = g_date
        
        for t in event_obj["TIME"]:
            i = event_obj["TIME"].index(t)
            g_time = text_processing.ProcessTimeTo12HFormat(time_text=str(t))
            event_obj["TIME"][i] = g_time

    print("------------------------------------------------------------------------------")
    ner_Interface.PrintEvents(events)

    print("------------------------------------------------------------------------------")
    print("Creating calendar event ......")
    g_Interface = GoogleCalendarInterface(establish_connection=False)
    google_events = []

    for e in events:
        n_event = g_Interface.CreateGoogleEvent(event=str(e["EVENT"]), 
                                                location=str(e["LOC"]), 
                                                time=e["TIME"][0], 
                                                date=e["DATE"],
                                                )
        #print("Event")
        #print(n_event)
        google_events.append(n_event)
    
    if len(google_events) > 0:
        g_Interface.ConnectToGoogleCalendar()
        for g_event in google_events:
            g_Interface.CreateCalendarEvent(googleEvent=g_event)
    else:
        print("NO GOOGLE EVENTS IN LIST")
    print("------------------------------------------------------------------------------")
    print("Done!")

def main():    
    SingleEventTest()
    pass

if __name__ == "__main__":
    main()