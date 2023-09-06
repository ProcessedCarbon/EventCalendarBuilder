from tkinter import *
from tkinter import ttk

class GUIInterface:
    def __init__(self):
        self.root = Tk()

    def CreateAppScreen(self,screen_width:int, screen_height:int, aspect=0.8):
        self.app_width = int(screen_width * aspect)
        self.app_height = int(screen_height * aspect)

        self.root.geometry(f"{str(self.app_width)}x{str(self.app_height)}")

    def CreateButton(self, on_click, text="Click"):
        myButton = ttk.Button(self.root, text=text, command=on_click)
        myButton.pack()
    
    def CreateLabel(self, text : str):
        myLabel = ttk.Label(self.root, text=text)
        myLabel.pack()

    def CreateEntry(self, width=50, default_text=""):
        textInput = ttk.Entry(self.root, width=width)

        if default_text != "" and default_text != " ":
            textInput.insert(0, default_text)

        textInput.pack()
    
    def CreateText(self, h : int, w : int)->Text:
        text = Text(self.root, height=h, width=w)
        text.pack()
        return text
    
    def RetrieveCurrentInputFromText(self, text:Text):
        input = text.get("1.0", END)
        return input
    
    def getSize(self)->tuple:
        return (self.app_width, self.app_height)

    def MainLoop(self):
        self.root.mainloop()




