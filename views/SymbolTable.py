import tkinter as tk
from tkinter import CENTER, END, NO, NSEW, ttk

from models.SymbolTableEntry import SymbolTableEntry

class SymbolTableView(tk.Toplevel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.config(width=700, height=450)
        self.title("Tabla de simbolos")
        self.resizable(False, False)

        self.focus()
        self.buildSymbolTable()
    
    def buildSymbolTable(self):
        # self.tbl = tk.Entry(self, width=20, fg='black', font=('Arial', 16, 'bold'), relief='groove')
        # self.tbl.grid(row=5, column=8, sticky=NSEW)
        self.tbl = ttk.Treeview(self, selectmode='browse')
        self.scrollb = ttk.Scrollbar(self, orient="vertical", command=self.tbl.yview)
        self.scrollb.pack(side='right', fill='x')
        self.tbl.configure(xscrollcommand=self.scrollb.set)
        self.tbl['columns'] = ('Variable', 'Tipo', 'Valor inicial', 'Alcance')
        self.tbl.column("#0", width=0, stretch=NO)
        self.tbl.column("Variable", anchor=CENTER, width=95)
        self.tbl.column("Tipo", anchor=CENTER, width=95)
        self.tbl.column("Valor inicial", anchor=CENTER, width=95)
        self.tbl.column("Alcance", anchor=CENTER, width=95)
        
        self.tbl.heading("#0", text="", anchor=CENTER)
        self.tbl.heading("Variable", text="Nombre", anchor=CENTER)
        self.tbl.heading("Tipo", text="Tipo", anchor=CENTER)
        self.tbl.heading("Valor inicial", text="Valor inicial", anchor=CENTER)
        self.tbl.heading("Alcance", text="Alcance", anchor=CENTER)
        
        self.tbl.pack()
    
    def insertToTable(self, varname, vartype, varvalue, varscope):
        self.tbl.insert(parent='',index='end',text='',values=(f'{varname}',f'{vartype}',f'{varvalue}', f'{varscope}'))
    
    def insertEntry(self, ste: SymbolTableEntry):
        self.tbl.insert(parent='', index='end', text='', values=(f'{ste.getName()}',f'{ste.getType()}',f'{ste.getInitValue()}', f'{ste.getScope()}'))
    
    def existsInTable(self, f: str):
        for child in self.tbl.get_children():
            print(child)
            
    def removeEntry(self):
        self.tbl.delete()
        
    def addToSymbolTable(self,type: str):
        self.tbl.insert(END, type)
        
    def pack(self):
        self.tbl.pack()
    
    
        