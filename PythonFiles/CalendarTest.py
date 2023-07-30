
import GoogleCalendarInterface
import NERInterface

from dateutil.parser import parse
import wordninja
import TextProcessing

def main():
    
    # g_Interface = GoogleCalendarInterface.Interface()
    ner_Interface = NERInterface.Interface()
    t = TextProcessing.Interface()

    test_text = "School of Civil and Environmental Engineering is offering EM5103 Water Resources Management to all NTU students to take as Unrestricted Elective (UE) or Broadening and Deepening Elective (BDE) in the Semester 1 AY2023-2024.For students who are keen to take the course as UE/BDE during Semester 1 AY2023-2024, you may register for it during Add/Drop period from Fri, 11 August 2023 – Fri, 25 August 2023 (10.30 am – 10.00 pm). Please ensure that you have sufficient UE/BDE balance AUs to take the course."

    # for f in formatted:
    #     print(f)

    # for ent in entities:
    #     print(ent.text + " ", ent.label_)

    # g_Interface.GetLatestCalendarEvent(count=10)

    # https://developers.google.com/calendar/api/v3/reference/events
    # CreateCalendarEvent(newEvent)

if __name__ == "__main__":
    main()
    
