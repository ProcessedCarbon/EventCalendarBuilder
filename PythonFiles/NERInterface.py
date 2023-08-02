import spacy

class NERInterface:
    def __init__(self):
        self.nlp = spacy.load(r"./model/model-best") #load model    
        self._event = None
        self._loc = None
        self._date = None
        self._time = None    
 
    def AssignEntities(self, text):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        self._event = None
        self._loc = None
        self._date = None
        self._time = None    

        doc = self.nlp(text) 
        entityList = list(doc.ents)

        if len(entityList) > 0 :
            for e in entityList:
                if e.label_ == "EVENT":
                    self._event = e
                elif e.label_ == "TIME":
                    self._time = e
                elif e.label_ == "DATE":
                    self._date = e
                elif e.label_ == "LOC":
                    self._loc = e

    def getEvent(self):
        return self._event
    
    def getLoc(self):
        return self._loc
    
    def getTime(self):
        return self._time
    
    def getDate(self):
        return self._date
