from GUI.GUIInterface import GUIInterface

class MiniPage():
    def __init__(self, size, parent, row=0, col=0, sticky='nsew') -> None:
        self.size = size
        self.parent = parent
        self.elements = []
        self.row = row
        self.col=col
        self.sticky=sticky
        
        tmp = GUIInterface.current_frame
        self.frame = GUIInterface.CreateFrame(parent)
        GUIInterface.CreateGrid(self.frame, rows=([1] * self.size), cols=[1])
        self.frame.grid(row=row, column=col, sticky=sticky)
        GUIInterface.current_frame = tmp

    def Queue(self, element)->bool:
        n = len(self.elements)
        if n < self.size:
            self.elements.append(element)
            return True
        return False

    def Pop(self):
        element = self.elements[len(self.elements) - 1]
        element.destroy()
        self.elements.remove(element)
        return element
    
    def getPage(self):
        return self.frame
    
    def getSize(self):
        return len(self.elements)
    
    def SwitchTo(self):
        #self.frame.tkraise()
        self.frame.grid(row=self.row, column=self.col, sticky=self.sticky)