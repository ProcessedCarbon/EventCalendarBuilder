import spacy
from Managers.ErrorConfig import ErrorCodes

class NERInterface:
    _error_code_list = ErrorCodes()._error_codes

    def __init__(self, model_path = r"./model/model-best" ):
        self.nlp = spacy.load(model_path) #load model       
 
    def GetEntitiesFromText(self, text:str):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        if text == None or "":
            print(f'[{str(self.__class__.__name__).upper()}](GetEntitiesFromText()): {self._error_code_list[1000]}')
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
                print(f"{str(entity)} - {entity.label_}")

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
    
    def getEntities(self, e : str, t : list, d : list, l : str):
        return {
            "EVENT" : e,
            "TIME" : t,
            "DATE" : d,
            "LOC" : l,
        }

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