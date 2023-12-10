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
    # from Managers.TextProcessing import TextProcessingManager
    # test_date = "23rd to 25th Aug"
    # print(TextProcessingManager.ProcessDate(test_date))
    from Managers.TextProcessing  import Test_ProcessTimeTo12HFormat
    Test_ProcessTimeTo12HFormat()

def OutlookTest():
    import Calendar.Outlook.OutlookInterface as outlook_interface
    outlook_interface.start()

    with open(r'./Testing/testing_text_r.txt') as f:
        content = f.read()
    f.close()
    from NER.NERInterface import NERInterface
    events = NERInterface.GetEntitiesFromText(content)
    # print("BEFORE")
    # for e in events: print(e)

    from Managers.TextProcessing import TextProcessingManager
    from Managers.DateTimeManager import DateTimeManager
    from Events.EventsManager import EventsManager

    for i in range(len(events)):
        date_time = events[i]["DATE_TIME"].copy()
        if len(date_time) == 0:
            curr_date = DateTimeManager.getCurrentDate()
            formatted_date = curr_date.strftime("%Y-%m-%d")
            events[i]["DATE_TIME"] = {formatted_date : [DateTimeManager.getCurrentTime()]}
            date = formatted_date
        else:
            for d in date_time:
                time = date_time[d]
                date = TextProcessingManager.ProcessDate(date_text=str(d))
                if len(time) > 0: n_time = TextProcessingManager.ProcessTime(time_text=str(time))
                else: n_time = [DateTimeManager.getCurrentTime()]

                events[i]["DATE_TIME"].pop(d)
                if isinstance(date, list) and len(date) > 1: 
                    for o in date: events[i]["DATE_TIME"][o] = n_time
                else: events[i]["DATE_TIME"][date] = n_time

        # Check how many dates event has, only create and end time if there is only
        # a single date else just treat that date pair as a range and sort them in ascending
        # Also handle the pairing of dates
        n = len(events[i]["DATE_TIME"])
        if n < 2:
            # If time only has start time get an end time
            for j in range(len(events[i]["DATE_TIME"][date])):

                new_time = [DateTimeManager.AddToTime(events[i]["DATE_TIME"][date][j], hrs=1)] if n > 0 else ["", ""]
                
                # Check if end time is greater than start time after adding if its smaller, minus by 1 hr 
                # and swap the first and new time 
                if new_time != ["", ""] and DateTimeManager.CompareTimes(str(new_time[0]), str(events[i]["DATE_TIME"][date][j])):
                    new_time = [DateTimeManager.AddToTime(events[i]["DATE_TIME"][date][j], hrs=-1)]
                    tmp = events[i]["DATE_TIME"][date]
                    events[i]["DATE_TIME"][date] = new_time
                    new_time = tmp

                events[i]["DATE_TIME"][date].extend(new_time)
        else: events[i]["DATE_TIME"] = dict(sorted(events[i]["DATE_TIME"].items()))

    # print("MID")
    # for e in events: print(e)

    print("------------------------------------------------------------------------------")
    print("Add to event manager list")
    for index, event in enumerate(events):
        # If more than 2 dates just ignore for now
        keys = list(events[index]['DATE_TIME'].keys())
        if len(keys) > 2:
            continue
    
        start_date = keys[0]
        end_date = start_date

        start_time = event['DATE_TIME'][start_date][0]
        end_time = start_time

        if len(keys) == 2: 
            end_date = keys[1]
            end_time = event['DATE_TIME'][end_date][0]
        else:
            if len(event['DATE_TIME'][end_date]) > 1: end_time = event['DATE_TIME'][end_date][1]

        n_event = EventsManager.CreateEventObj(id=index,
                                            name=event['EVENT'],
                                            location=event["LOC"],
                                            s_date=start_date,
                                            e_date=end_date,
                                            start_time=start_time,
                                            end_time=end_time)
        #print(vars(n_event))
        EventsManager.AddEventToEventDB(n_event, EventsManager.events)
        print(EventsManager.events)

    # print("AFTER")
    # for e in events: print(e)

def NERGroupTest():
    with open(r'./Testing/testing_text_grp.txt') as f:
        content = f.read()
    f.close()
    from NER.NERInterface import NERInterface
    from Events.EventsManager import EventsManager

    events = NERInterface.GetEntitiesFromText(content)
    print('================= RAW EVENTS ================= ')
    for e in events: print(e)
    print('================= PROCESSED EVENTS ================= ')
    p_events = EventsManager.ProcessEvents(events)
    for e in p_events: print(e)
    print('================= ADDED EVENTS ================= ')
    added_events = EventsManager.AddEvents(events=p_events)
    for e in added_events: print(e)

def main():    
    #TestInstall()
    #MacCalendarTest()
    #TextProcessingManagerTest()
    #OutlookTest()
    NERGroupTest()
    pass

if __name__ == "__main__":
    main()