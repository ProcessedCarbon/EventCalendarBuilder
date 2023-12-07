import spacy
from Managers.ErrorConfig import ErrorCodes

model_path = r"./model/model-best"

class NERInterface:
    nlp = spacy.load(model_path) #load model   

    # Extracts entities from given text
    def GetEntitiesFromText(text:str):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        if text == None or "":
            ErrorCodes.PrintErrorWithCode(1000)
            return

        doc = NERInterface.nlp(text) 
        entityList = list(doc.ents)
        events = []                

        if len(entityList) > 0 :
            # tmp_date_list = []
            tmp_time_list = []
            loc = ""
            event_name = ""
            curr_dt =None
            dt = {}

            for entity in entityList:
                #print(f"{str(entity)} - {entity.label_}")

                e = str(entity)
                if entity.label_ == "E_NAME":
                    if event_name != e:

                        # To handle if first entity in list is event
                        if event_name == "":
                            event_name = e
                            continue

                        events.append(NERInterface.getEntities(e=event_name, dt=dt, l=loc))
                        # tmp_date_list = []
                        tmp_time_list = []
                        dt ={}
                        dt_list = []
                        curr_dt = None
                        loc = ""
                        event_name = e

                elif entity.label_ == "E_DATE":
                    # Already encountered a time label before date
                    if len(tmp_time_list) > 0 and curr_dt != None:
                        dt[curr_dt] = tmp_time_list
                        tmp_time_list = []
                        #dt_list.append(dt)
                    curr_dt = entity
                    dt[curr_dt] = tmp_time_list
                    #tmp_date_list.append(e)

                elif entity.label_ == "E_TIME":
                    # Handle already encountered date
                    if curr_dt != None: dt[curr_dt].append(e)
                    else: tmp_time_list.append(e)

                elif entity.label_ == "E_LOC":
                    loc = e
                
                # Append what is left and return list of events
                if entity == entityList[-1] and entity.label_ != "E_NAME":
                    events.append(NERInterface.getEntities(e=event_name, dt=dt, l=loc))
                    return events
                
        return events
    
    # Creates NER entity dataype
    def getEntities(e : str, dt : list, l : str):
        return {
            "EVENT" : e,
            "DATE_TIME" : dt,
            "LOC" : l,
        }

    def getSingleEntity(e:str, t:list[str], d:str, l:str):
        return {
            "EVENT" : e,
            "TIME" : t,
            "DATE" : d,
            "LOC" : l,
        }

    # Returns a list of event with single date time pairing
    # def HandleEventDateTimeMapping(event_list:list[dict])->list:
    #     """
    #     Maps each date in an event to a time. Ignores extras for both date
    #     and time.
    #     """
    #     processed_events = []
    #     for e in event_list:
    #         for i in range(len(e['DATE_TIME'])):
    #             for d in e['DATE_TIME'][i]:
    #             new_event = NERInterface.getSingleEntity(e=e["EVENT"], 
    #                                                     t=e['DATE_TIME'][i],
    #                                                     d=d, 
    #                                                     l=e["LOC"])                
    #         #processed_events.append(new_event)
    #     return processed_events
        
def main():
    NER = NERInterface()

    # testing_file_path = "./Testing/testing_text_r.txt"
    # def getTestingText():
    #     with open(testing_file_path, encoding='utf-8') as f:
    #         lines = f.read().replace('\n', '')
        
    #     return lines
    
    # test_text = getTestingText()
    # events = NER.GetEntitiesFromText(text=test_text)

    # def PrintEvent(event_obj):
    #     event = event_obj["EVENT"]
    #     location = event_obj["LOC"]
    #     date = event_obj["DATE"]
    #     time = event_obj["TIME"]

    #     print("------------------------------------------------------------------------------")
    #     print("event: ", event)
    #     print("location: ", location)
    #     print("date: ", date)
    #     print("time: ", time)
    
    # for e in events:
    #     PrintEvent(e)

if __name__ == "__main__":
    main()