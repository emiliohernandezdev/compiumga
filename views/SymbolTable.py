import tkinter as tk

class SymbolTableView(tk.Toplevel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=500, height=450)
        self.title("Tabla de simbolos")
        self.resizable(False, False)
        
        self.focus()
        self.grab_set()
    
    def buildSymbolTable(self):
        tbl = tk.Entry(self, width=15, fg='black')
        tbl.grid(row=5, column=8)
        