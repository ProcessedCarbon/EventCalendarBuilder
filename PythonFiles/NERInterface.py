import spacy

class Interface:
    def __init__(self):
        self.nlp = spacy.load(r"./model/model-best") #load model        
 
    def GetEntities(self, text):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        doc = self.nlp(text) 
        entityList = list(doc.ents)

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

        return event, time, date, loc


