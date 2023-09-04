from tkinter import *
from tkinter import ttk

class GUIInterface:
    def __init__(self, default_size="380x400"):
        self.root = Tk()
        self.root.geometry(default_size)

    def CreateButton(self, on_click):
        myButton = ttk.Button(self.root, text="Click", command=on_click)
        myButton.pack()
    
    def CreateLabel(self, text : str):
        myLabel = ttk.Label(self.root, text=text)
        myLabel.pack()

    def CreateEntry(self, width=50, default_text=""):
        textInput = ttk.Entry(self.root, width=width)

        if default_text != "" and default_text != " ":
            textInput.insert(0, default_text)

        textInput.pack()

    def MainLoop(self):
        self.root.mainloop()




