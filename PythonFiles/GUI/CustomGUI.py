from customtkinter import *
from Managers.ErrorConfig import getParamValFromKwarg
from GUI.GUIInterface import GUIInterface

class CustomGUI:
    def __init__(self) -> None:
        pass

    def CreateEntryWithLabel(label:str, **kwargs)->list[CTkFrame, CTkLabel, CTkEntry]:
        entry_width =       getParamValFromKwarg('entry_width', kwargs)
        default_text =      getParamValFromKwarg('default_text', kwargs)

        tmp_frame = GUIInterface.current_frame
        entry_frame = GUIInterface.CreateFrame(frame_target=GUIInterface.current_frame)

        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=3)

        # Entry label
        label = GUIInterface.CreateLabel(text=label)
        label.grid(row=0, column=0)

        # Entry
        entry = GUIInterface.CreateEntry(width=entry_width, textvariable=default_text)
        entry.grid(row=0, column=1, sticky='e')

        GUIInterface.SetCurrentFrame(tmp_frame)

        return entry_frame, label ,entry
    
    def CreateComboboxWithLabel(label:str, dropdown:list[str])->list[CTkFrame,CTkLabel,CTkComboBox]:    
        tmp_frame = GUIInterface.current_frame
        combo_frame = GUIInterface.CreateFrame(frame_target=GUIInterface.current_frame)

        combo_frame.columnconfigure(0, weight=1)
        combo_frame.columnconfigure(1, weight=3)

        # Entry label
        label = GUIInterface.CreateLabel(text=label)
        label.grid(row=0, column=0, sticky='w')

        # Entry
        combobox = GUIInterface.CreateComboBox(values=dropdown)
        combobox.grid(row=0, column=1)

        GUIInterface.SetCurrentFrame(tmp_frame)

        return combo_frame, label, combobox

