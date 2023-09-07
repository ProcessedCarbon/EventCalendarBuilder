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

    def CreateButton(self,on_click, text="Click"):
        myButton = ttk.Button(self.current_frame, text=text, command=on_click)
        myButton.pack()
    
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
    
    def RetrieveCurrentInputFromText(self, text:Text):
        input = text.get("1.0", END)
        return input
    
    def getSize(self)->tuple:
        return (self.app_width, self.app_height)

    def SetCurrentFrame(self, frame):
        self.current_frame = frame

    def MainLoop(self):
        self.root.mainloop()




