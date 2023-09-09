import spacy
from Managers.ErrorConfig import ErrorCodes

class NERInterface:
    def __init__(self, model_path = r"./model/model-best" ):
        self.nlp = spacy.load(model_path) #load model       
 
    # Extracts entities from given text
    def GetEntitiesFromText(self, text:str):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        if text == None or "":
            ErrorCodes.PrintErrorWithCode(1000)
            return

        doc = self.nlp(text) 
        entityList = list(doc.ents)

        if len(entityList) > 0 :
            tmp_date_list = []
            tmp_time_list = []
            loc = None
            event_name = None # None is used in the event str(entity) == ""

            events = []                

            for entity in entityList:
                #print(f"{str(entity)} - {entity.label_}")

                e = str(entity)
                if entity.label_ == "EVENT":
                    if event_name != e:

                        # To handle if first entity in list is event
                        if event_name == None:
                            event_name = e
                            continue
                        
                        events.append(self.getEntities(e=event_name, t=tmp_time_list, d=tmp_date_list, l=loc))
                        tmp_date_list = []
                        tmp_time_list = []
                        loc = None
                        event_name = e

                elif entity.label_ == "DATE":
                    tmp_date_list.append(e)

                elif entity.label_ == "TIME":
                    tmp_time_list.append(e)

                elif entity.label_ == "LOC":
                    loc = e
                
                # Append what is left and return list of events
                if entity == entityList[-1] and entity.label_ != "EVENT":
                    events.append(self.getEntities(e=event_name, t=tmp_time_list, d=tmp_date_list, l=loc))
                    return events
                
        return events
    
    # Creates NER entity dataype
    def getEntities(self, e : str, t : list, d : list, l : str):
        return {
            "EVENT" : e,
            "TIME" : t,
            "DATE" : d,
            "LOC" : l,
        }

    def getSingleEntity(self, e:str, t:str, d:str, l:str):
        return {
            "EVENT" : e,
            "TIME" : t,
            "DATE" : d,
            "LOC" : l,
        }
    
    # Prints entity per event in list
    def PrintEvents(self, events : list[dict]):
        for e in events:
            event = e["EVENT"]
            location = e["LOC"]
            date = e["DATE"]
            time = e["TIME"]

            print("------------------------------------------------------------------------------")
            print("event: ", event)
            print("location: ", location)
            print("date: ", date)
            print("time: ", time)

    # Returns a list of event with single date time pairing
    def ProcessEvents(self,event_list:list[dict])->list:
        """
        Per date in each event in event_list, creates a single date time pairing and
        creates  duplicate of that event
        """
        processed_events = []
        for e in event_list:
            for d in e["DATE"]:
                for t in e["TIME"]:
                    new_event = self.getSingleEntity(e=e["EVENT"], t=t,d=d, l=e["LOC"])
                    processed_events.append(new_event)
        return processed_events
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