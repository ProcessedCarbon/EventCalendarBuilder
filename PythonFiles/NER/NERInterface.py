import spacy
import logging
from uuid import uuid4

import Managers.DirectoryManager as directory_manager
from NER.NER_Constants import NAME, DATE, TIME, LOC, DESC, BASE_MODEL, BASE_MODEL_W_DESC

PARENT_DIR = directory_manager.getCurrentFileDirectory(__file__)
MODEL_PATH = directory_manager.getFilePath(PARENT_DIR, f'model/{BASE_MODEL_W_DESC}')

class NERInterface:
    nlp = spacy.load(MODEL_PATH) #load model   

    # Extracts entities from given text
    def GetEntitiesFromText(text:str):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        if text == None or "":
            logging.error(f"[{__name__}] INVALID PARAM GIVEN!")
            return

        doc = NERInterface.nlp(text) 
        entityList = list(doc.ents)
        events = []                

        if len(entityList) > 0 :
            tmp_time_list = []
            loc = ""
            event_name = ""
            curr_dt =None
            dt = {}
            desc = ""
            # copy_dict = entityList.copy()

            for entity in entityList:
                e = str(entity)
                if entity.label_ == NAME:
                    if event_name != e:

                        # To handle if first entity in list is event
                        if event_name == "":
                            event_name = e
                            continue

                        events.append(NERInterface.getEntities(e=event_name, dt=dt, l=loc, d=desc))
                        tmp_time_list = []
                        dt ={}
                        curr_dt = None
                        loc = ""
                        desc = ""
                        event_name = e # set name to the next entity

                elif entity.label_ == DATE:
                    # Already encountered a time label before date
                    if len(tmp_time_list) > 0 and curr_dt != None:
                        dt[curr_dt] = tmp_time_list
                        tmp_time_list = []
                    curr_dt = entity
                    dt[curr_dt] = tmp_time_list

                elif entity.label_ == TIME:
                    # Handle already encountered date
                    if curr_dt != None: dt[curr_dt].append(e)
                    else: tmp_time_list.append(e)

                elif entity.label_ == LOC:
                    loc = e
                
                elif entity.label_ == DESC:
                    desc += e
                
                # Append what is left and return list of events
                if entity == entityList[-1] and entity.label_ != NAME:
                    events.append(NERInterface.getEntities(e=event_name, dt=dt, l=loc, d=desc))
                    return events
                
        return events
    
    # Creates NER entity dataype
    def getEntities(e:str, dt:list, l:str, d:str):
        return {
            "EVENT" : e,
            "DATE_TIME" : dt,
            "LOC" : l,
            "DESC": d
        }