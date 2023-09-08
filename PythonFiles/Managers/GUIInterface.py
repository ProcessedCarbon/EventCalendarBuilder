from tkinter import *
from tkinter import ttk

class GUIInterface:
    def __init__(self):
        self.root = Tk()
        self.main_frame = self.CreateFrame(frame_target=self.root)
        self.current_frame = self.main_frame
        self.main_frame.pack(fill=BOTH, expand=True)

    def CreateAppScreen(self, screen_width:int, screen_height:int, aspect=0.8):
        self.app_width = int(screen_width * aspect)
        self.app_height = int(screen_height * aspect)
        self.root.geometry(f"{str(self.app_width)}x{str(self.app_height)}")

    def CreateButton(self,on_click, text="Click", pack_side=TOP, pack_anchor:str=""):
        myButton = ttk.Button(self.current_frame, text=text, command=on_click)
        myButton.pack(side=pack_side, anchor=pack_anchor)
    
    def CreateLabel(self,text : str, font_type:str="", font_size:int=0):
        myLabel = ttk.Label(self.current_frame, text=text, font=(font_type, font_size))
        myLabel.pack()

    def CreateEntry(self,width=50, default_text=""):
        textInput = ttk.Entry(self.current_frame, width=width)

        if default_text != "" and default_text != " ":
            textInput.insert(0, default_text)

        textInput.pack()
    
    def CreateText(self,h : int, w : int)->Text:
        text = Text(self.current_frame, height=h, width=w)
        text.pack()
        return text
    
    def CreateFrame(self, frame_target)->ttk.Frame:
        frame = ttk.Frame(frame_target)
        return frame
    
    def CreateEntryWithLabel(self, frame_target, label:str, frame_row:int, frame_col:int, padx:int=0, pady:int=0):
        entry_frame = ttk.Frame(frame_target)

        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=3)

        # Entry label
        label = ttk.Label(entry_frame, text=label)
        label.grid(row=0, column=0, sticky=E)

        # Entry
        entry = ttk.Entry(entry_frame, width=50)
        entry.grid(row=0, column=1, sticky=W)

        entry_frame.grid(row=frame_row, column=frame_col, padx=padx, pady=pady)

    def RetrieveCurrentInputFromText(self, text:Text):
        input = text.get("1.0", END)
        return input
    
    def getSize(self)->tuple:
        return (self.app_width, self.app_height)

    def SetCurrentFrame(self, frame):
        self.current_frame = frame

    def MainLoop(self):
        self.root.mainloop()




