from tkinter import *
from customtkinter import *
from typing import Tuple    

class GUIInterface:
    current_frame = None    
    root = CTk()

    def CreateFrame(frame_target, b_color='', b_width=0, fg_color='transparent')->CTkFrame:
        frame = CTkFrame(frame_target, fg_color=fg_color, border_color=b_color, border_width=b_width)
        GUIInterface.SetCurrentFrame(frame)
        return frame
    
    def CreateButton(on_click, text="Click")->CTkButton:
        myButton = CTkButton(GUIInterface.current_frame, text=text, command=on_click, corner_radius=10)
        return myButton
        
    def CreateLabel(text : str, font=("",0))->CTkLabel:
        myLabel = CTkLabel(GUIInterface.current_frame, text=text, font=font)
        return myLabel

    def CreateEntry(width=50, default_text="", place_holder_text="", place_holder_color="grey")->CTkEntry:
        textInput = CTkEntry(GUIInterface.current_frame, 
                             width=width, 
                             textvariable=default_text,
                             placeholder_text=place_holder_text, 
                             placeholder_text_color=place_holder_color)
        return textInput
    
    def CreateText(h : int, w : int)->CTkTextbox:
        text = CTkTextbox(GUIInterface.current_frame, height=h, width=w)
        return text
    
    def CreateComboBox(values:list[str])->CTkComboBox:
        combobox = CTkComboBox(GUIInterface.current_frame, values=values, state='readonly')
        return combobox

    # frame_row:int, padx=0, pady=0, gap=10, default_text=""
    def CreateEntryWithLabel(label:str, **kwargs)->CTkEntry:
        entry_width = kwargs["entry_width"] if "entry_width" in kwargs else 0
        entry_percent = kwargs["entry_percent"] if "entry_percent" in kwargs else 0.5
        default_text = kwargs["default_text"] if "default_text" in kwargs else ""
        frame_row = kwargs["frame_row"] if "frame_row" in kwargs else 0
        padx = kwargs["padx"] if "padx" in kwargs else 0
        pady = kwargs["pady"] if "pady" in kwargs else 0
        gap = kwargs["gap"] if "gap" in kwargs else 10
        
        tmp_frame = GUIInterface.current_frame
        entry_frame = GUIInterface.CreateFrame(frame_target=GUIInterface.current_frame)

        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=3)

        # Entry label
        label = GUIInterface.CreateLabel(text=label)
        label.grid(row=0, column=0)

        # Entry
        entry = GUIInterface.CreateEntry(width=entry_width * entry_percent, default_text=default_text)
        entry.grid(row=0, column=1, sticky=E)

        entry_frame.grid(row=frame_row, padx=padx, pady=pady, sticky=NSEW, ipadx=gap)

        GUIInterface.SetCurrentFrame(tmp_frame)

        return entry

    def CreateGrid(target:CTkFrame, rows=1, cols=1):
        for i in range(rows):
            target.rowconfigure(i, weight=1)
        
        for i in range(cols):
            target.columnconfigure(i, weight=1)

    def UpdateEntry(entry:CTkEntry, text_var:str):
        entry.delete(0, END)
        entry.insert(0, text_var)
        
    def RetrieveCurrentInputFromTextbox(text:CTkTextbox):
        input = text.get("0.0", END)
        return input
    
    def ClearCurrentFrame():
        GUIInterface.current_frame = None

    def SetCurrentFrame(frame):
        GUIInterface.current_frame = frame

    def MainLoop(self):
        self.root.mainloop()




