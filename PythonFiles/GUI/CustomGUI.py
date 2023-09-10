from customtkinter import *
from Managers.ErrorConfig import getParamValFromKwarg
from GUI.GUIInterface import GUIInterface

class CustomGUI:
    def __init__(self) -> None:
        pass

    def CreateEntryWithLabel(label:str, **kwargs)->CTkEntry:
        entry_width =       getParamValFromKwarg('entry_width', kwargs)
        entry_percent =     getParamValFromKwarg('entry_percent', kwargs, default=0.5)
        default_text =      getParamValFromKwarg('default_text', kwargs)
        frame_row =         getParamValFromKwarg('frame_row', kwargs, default=0)
        padx =              getParamValFromKwarg('padx', kwargs, default=0)
        pady =              getParamValFromKwarg('pady', kwargs, default=0)
        gap =               getParamValFromKwarg('gap', kwargs, default=10)
        
        tmp_frame = GUIInterface.current_frame
        entry_frame = GUIInterface.CreateFrame(frame_target=GUIInterface.current_frame)

        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=3)

        # Entry label
        label = GUIInterface.CreateLabel(text=label)
        label.grid(row=0, column=0)

        # Entry
        entry = GUIInterface.CreateEntry(width=entry_width * entry_percent, textvariable=default_text)
        entry.grid(row=0, column=1, sticky='e')

        entry_frame.grid(row=frame_row, padx=padx, pady=pady, sticky='nsew', ipadx=gap)

        GUIInterface.SetCurrentFrame(tmp_frame)

        return entry
