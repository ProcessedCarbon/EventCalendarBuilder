from tkinter import *
from customtkinter import *

class GUIInterface:
    def __init__(self):
        self.root = CTk()
        self.main_frame = self.CreateFrame(frame_target=self.root)
        self.SetCurrentFrame(self.main_frame)
        self.main_frame.pack(fill=BOTH, expand=True)

    def CreateAppScreen(self, screen_width:int, screen_height:int, aspect=0.8):
        self.app_width = int(screen_width * aspect)
        self.app_height = int(screen_height * aspect)
        self.root.geometry(f"{str(self.app_width)}x{str(self.app_height)}")

    def CreateButton(self,on_click, text="Click")->CTkButton:
        myButton = CTkButton(self.current_frame, text=text, command=on_click, corner_radius=10)
        return myButton
        
    def CreateLabel(self,text : str, font=("",0))->CTkLabel:
        myLabel = CTkLabel(self.current_frame, text=text, font=font)
        return myLabel

    def CreateEntry(self,width=50, default_text="")->CTkEntry:
        textInput = CTkEntry(self.current_frame, width=width)

        if default_text != "" and default_text != " ":
            textInput.insert(0, default_text)

        return textInput
    
    def CreateText(self,h : int, w : int)->Text:
        text = Text(self.current_frame, height=h, width=w)
        return text
    
    def CreateFrame(self, frame_target, b_color:str='', b_width:int=0, fg_color:str='transparent')->CTkFrame:
        frame = CTkFrame(frame_target, fg_color=fg_color, border_color=b_color, border_width=b_width)
        return frame
    
    def CreateEntryWithLabel(self, frame_target, label:str, frame_row:int, padx:int=0, pady:int=0, gap:int=10):
        entry_frame = self.CreateFrame(frame_target=frame_target)
        self.SetCurrentFrame(entry_frame)

        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=3)

        # Entry label
        label = self.CreateLabel(text=label)
        label.grid(row=0, column=0)

        # Entry
        entry = self.CreateEntry(self.app_width * 0.5)
        entry.grid(row=0, column=1, sticky=E)

        entry_frame.grid(row=frame_row, padx=padx, pady=pady, sticky=NSEW, ipadx=gap)
        self.ClearCurrentFrame()

    def RetrieveCurrentInputFromText(self, text:Text):
        input = text.get("1.0", END)
        return input
    
    def getSize(self)->tuple:
        return (self.app_width, self.app_height)

    def ClearCurrentFrame(self):
        self.current_frame=None

    def SetCurrentFrame(self, frame):
        self.current_frame = frame

    def MainLoop(self):
        self.root.mainloop()




