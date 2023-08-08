
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from TextProcessing import TextProcessingManager

testing_file_path = "./Testing/testing_text_r.txt"

def getTestingText():
    with open(testing_file_path, encoding='utf-8') as f:
        lines = f.read().replace('\n', '')
    
    return lines

def main():    
    print("------------------------------------------------------------------------------")
    print("Reading testing text in progress....")
    test_text = getTestingText()
    print(test_text)
    print("------------------------------------------------------------------------------")
    print("Reading Done!")

    print("------------------------------------------------------------------------------")
    print("Getting Entities from text.....")
    ner_Interface = NERInterface()
    events = ner_Interface.GetEntitiesFromText(text=test_text)

    def PrintEvent(event_obj):
        event = event_obj["EVENT"]
        location = event_obj["LOC"]
        date = event_obj["DATE"]
        time = event_obj["TIME"]

        print("------------------------------------------------------------------------------")
        print("event: ", event)
        print("location: ", location)
        print("date: ", date)
        print("time: ", time)
    
    for e in events:
        PrintEvent(e)

    print("------------------------------------------------------------------------------")
    print("Processing text to google format ...... ")
    text_processing = TextProcessingManager()

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
    for e in events:
        PrintEvent(e)

    # print("------------------------------------------------------------------------------")
    # print("Creating calendar event ......")
    # g_Interface = GoogleCalendarInterface(establish_connection=False)
    # n_event = g_Interface.CreateGoogleEvent(event=str(event), 
    #                                           location=str(location), 
    #                                           time=google_time, 
    #                                           date=google_date,
    #                                           )
    # print("Event")
    # print(n_event)
    # g_Interface.ConnectToGoogleCalendar()
    # g_Interface.CreateCalendarEvent(googleEvent=n_event)
    # print("------------------------------------------------------------------------------")
    # print("Done!")

if __name__ == "__main__":
    main()
    
