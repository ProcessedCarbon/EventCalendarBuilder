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

        event = time = date = loc = ""

        if len(entityList) > 0 :
            for e in entityList:
                if e.label_ == "EVENT":
                    event = e
                elif e.label_ == "TIME":
                    time = e
                elif e.label_ == "DATE":
                    date = e
                elif e.label_ == "LOC":
                    loc = e

        return self.getEntities(e=event, t=time, d=date, l=loc)
    
    def getEntities(self, e : str, t : str, d : str, l : str):
        return {
            "EVENT" : e,
            "TIME" : t,
            "DATE" : d,
            "LOC" : l,
        }