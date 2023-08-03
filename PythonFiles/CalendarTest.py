
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from TextProcessing import TextProcessingManager

from dateutil.parser import parse

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
    ner_Interface.AssignEntities(text=test_text)
    event = ner_Interface.getEvent()
    location = ner_Interface.getLoc()
    date = ner_Interface.getDate()
    time = ner_Interface.getTime()

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
    # g_Interface = GoogleCalendarInterface()
    # n_event = g_Interface.CreateGoogleEvent(event=str(event), 
    #                                           location=str(location), 
    #                                           time_start=str(google_time[0]), 
    #                                           time_end=str(google_time[1]),
    #                                           date_start=str(google_date[0]),
    #                                           date_end=None
    #                                           )
    # print("Event")
    # print(n_event)
    # g_Interface.CreateCalendarEvent(new_event=n_event)
    # print("------------------------------------------------------------------------------")
    # print("Done!")

if __name__ == "__main__":
    main()
    
