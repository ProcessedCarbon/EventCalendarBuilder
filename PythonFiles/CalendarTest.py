
from GoogleCalendarInterface import GoogleCalendarInterface
from NERInterface import NERInterface
from Managers.TextProcessing import TextProcessingManager

from dateutil.parser import parse

testing_file_path = "./Testing/testing_text_r.txt"

def getTestingText():
    with open(testing_file_path, encoding='utf-8') as f:
        lines = f.read().replace('\n', '')
    
    return lines

def main():
    
    print("------------------------------------------------------------------------------")
    print("Initializing Interfaces in progress.......")
    g_Interface = GoogleCalendarInterface()
    ner_Interface = NERInterface()
    text_processing = TextProcessingManager()

    print("------------------------------------------------------------------------------")
    print("Initialization Done!")
    #test_text = "School of Civil and Environmental Engineering is offering EM5103 Water Resources Management to all NTU students to take as Unrestricted Elective (UE) or Broadening and Deepening Elective (BDE) in the Semester 1 AY2023-2024.For students who are keen to take the course as UE/BDE during Semester 1 AY2023-2024, you may register for it during Add/Drop period from Fri, 11 August 2023 – Fri, 25 August 2023 (10.30 am – 10.00 pm). Please ensure that you have sufficient UE/BDE balance AUs to take the course."
    
    print("------------------------------------------------------------------------------")
    print("Reading testing text in progress....")
    test_text = getTestingText()
    print("------------------------------------------------------------------------------")
    print("Reading Done!")

    print("------------------------------------------------------------------------------")
    print("Getting Entities from text.....")
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
    google_time = text_processing.ProcessTimeForGoogleCalendars(time_text=str(time))
    google_date = text_processing.ProcessDateForGoogleCalendar(date_text=str(date))

    print("------------------------------------------------------------------------------")
    print("Google Time: ", google_time)
    print("Google Date: ", google_date)

    print("------------------------------------------------------------------------------")
    print("Creating calendar event ......")
    n_event = g_Interface.CreateGoogleEvent(event=str(event), 
                                              location=str(location), 
                                              time_start=str(google_time[0]), 
                                              time_end=str(google_time[1]),
                                              date_start=str(google_date[0]),
                                              date_end=None
                                              )
    print("Event")
    print(n_event)
    g_Interface.CreateCalendarEvent(new_event=n_event)
    print("------------------------------------------------------------------------------")
    print("Done!")

if __name__ == "__main__":
    main()
    
