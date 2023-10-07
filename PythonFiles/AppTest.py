import os
from pathlib import Path
os.chdir(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

# Extracts text from plain text file 
def getTestingText(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.read()
    
    return lines

def TestInstall():
    import os
    os.system('pip freeze > requirements.txt')

def MacCalendarTest():
    import Calendar.CalendarMacInterface as mac_calendar
    mac_calendar.getMacCalendarEvents()

def TextProcessingManagerTest():
    from Managers.TextProcessing import TextProcessingManager
    test_date = "23rd to 25th Aug"
    print(TextProcessingManager.ProcessDate(test_date))

def main():    
    TestInstall()
    #MacCalendarTest()
    #TextProcessingManagerTest()
    pass

if __name__ == "__main__":
    main()