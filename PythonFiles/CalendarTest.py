
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
    entities = ner_Interface.GetEntitiesFromText(text=test_text)

    event = entities["EVENT"]
    location = entities["LOC"]
    date = entities["DATE"]
    time = entities["TIME"]

    print("------------------------------------------------------------------------------")
    print("event: ", event)
    print("location: ", location)
    print("date: ", date)
    print("time: ", time)

    print("------------------------------------------------------------------------------")
    print("Processing text to google format ...... ")
    text_processing = TextProcessingManager()
    google_time = text_processing.ProcessTimeForGoogleCalendars(time_text=str(time))
    google_date = text_processing.ProcessDateForGoogleCalendar(date_text=str(date))

    print("------------------------------------------------------------------------------")
    print("Google Time: ", google_time)
    print("Google Date: ", google_date)

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
    
