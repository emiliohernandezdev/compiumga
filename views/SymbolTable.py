import tkinter as tk

class SymbolTableView:
    
    def __init__(self, title: str) -> tk.Tk:
        self.view = tk.Tk()
        self.view.geometry('800x600')
        self.view.po
        self.view.resizable(False, False)
        
        self.view.title(title)
        
        return self.view