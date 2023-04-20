import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import END, scrolledtext as st
from libs.Core import Core
from libs.Keyword import Keyword
from libs.Operator import Operator
from libs.DataType import DataType
from views.SymbolTable import SymbolTableView

class Analyzer:
    currentPath = ''
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1160x600")
        self.window.resizable(False, False)
        
        self.menu = tk.Menu(self.window)
        
        self.setTitle()
        self.buildMenu()
        self.buildGrid()
        self.clenControls()
        self.currentFile = None
        
        self.window.mainloop()
        
    def setTitle(self):
        self.window.title("Compiladores / Emilio Hernández")
        
    def cleanFileAndPath(self):
        self.currentFile = None
        self.currentPath = ''
        
    def buildGrid(self):

        self.txt1 = st.ScrolledText(self.window, width=45, height=25)
        self.txt1.grid(column=0, row=0, padx=5, pady=5)
        self.txt1.delete('1.0', END);

        self.txt2 = st.ScrolledText(self.window, width=90, height=25)
        self.txt2.grid(column=1, row=0, padx=5, pady=5)
        
        self.txt3 = st.ScrolledText(self.window, width=135, height=10)
        self.txt3.grid(columnspan=2, column=0, row=1, padx=5, pady=10)
    
    def clenControls(self):
        
        self.txt1.delete('1.0', END)
        self.txt2.delete('1.0', END)
        self.txt3.delete('1.0', END)

    def buildMenu(self):

        self.window.config(menu=self.menu)
        options = tk.Menu(self.menu, tearoff=0)
        execution = tk.Menu(self.menu, tearoff=0)
        options.add_command(label="Abrir", command=self.open)
        options.add_command(label="Guardar", command=self.save)
        options.add_command(label="Guardar como...", command=self.saveAs)
        options.add_command(label="Tabla de Simbolos", command=self.exit)
        options.add_separator()
        options.add_command(label="Salir", command=self.exit)
        execution.add_command(label="Compilar", command=self.businessProcess)
        self.menu.add_cascade(label="Archivo", menu=options)
        self.menu.add_cascade(label="Ejecucion", menu=execution)
        
    def open(self):
        if self.currentPath == '':   
            try:
                self.window.title("Abrir archivo...")
                file = filedialog.askopenfilename(
                    title="Abrir archivo a compilar...",
                    defaultextension=".txt",
                    filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"),),
                )

                with open(file, 'r') as f:
                    content = f.read()
                    self.window.title("Compilar - " + file)
                    self.currentPath = file
                    self.txt1.delete('1.0', END)
                    self.txt1.insert('1.0', content)
                    self.txt1.edit_modified(0)
                
            except Exception as e:
                messagebox.showerror("Error al abrir el archivo", e)
                self.cleanFileAndPath()
        else:
            if self.txt1.edit_modified():
                resp = self.askSave()
                if resp == 'yes':
                    self.saveAs()
                elif resp == 'no':
                    self.cleanFileAndPath()
                    self.open()
            else:
                self.save()
                self.cleanFileAndPath()
                self.open()
            
    def askSave(self):
        quest = messagebox.askquestion("Guardar archivo", "El archivo no ha sido guardado, desea guardarlo?")
        return quest
            
                
        
    def save(self):
        if self.currentPath == '' and self.txt1.edit_modified() == 0:
            messagebox.showerror("Guardar", "No se ha abierto ningún archivo")
        elif self.currentPath == '' and self.txt1.edit_modified() == 1:
            self.saveAs()
        else:
            try:
                if self.currentPath != "":
                    with open(self.currentPath, 'w') as f:
                        content = self.txt1.get('1.0', END)
                        f.write(content)
                        f.close()
                        messagebox.showinfo("Guardar archivo", "El archivo se guardó de manera correcta en: " + self.currentPath)
                        #self.txt1.delete('1.0', END)
                        self.setTitle()
                        #self.cleanFileAndPath()
                    
            except Exception as e:
                messagebox.showerror("Error al guardar el archivo", e)
                self.cleanFileAndPath()
            
    def saveAs(self):
        if self.currentPath == '' and self.txt1.edit_modified() == 0:
            messagebox.showerror("Guardar como...", "No se ha abierto ningún archivo")
            return
        else:
            try:
                file = filedialog.asksaveasfile(
                    title ="Guardar como...",
                    defaultextension=".txt",
                    filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"),
                ))
                currentInput = self.txt1.get('1.0', END)
                file.write(currentInput)
                file.close()
                messagebox.showinfo("Guardar archivo", "El archivo se guardó correctamente")
                self.setTitle()
                self.cleanFileAndPath()
            except Exception as e:
                self.cleanFileAndPath()
                messagebox.showerror("Error al guardar el archivo", str(e))
                
                
    def businessProcess(self):
        self.txt2.delete(1.0, END)
        lines = self.txt1.get('1.0', END)
        
        tokens = []
        
        kw = Keyword()
        op = Operator()
        
        for line in lines.split('\n'):
            i = 0
            # line = line.strip()
            while i < len(line):
                char = line[i]
                if char.isdigit():
                    j = i + 1
                    while j < len(line) and (line[j].isdigit() or line[j] == "."):
                        j += 1
                    token = line[i:j]
                    self.txt2.insert(END, f'NUM({token})\n')
                    i = j
                elif char.isalpha() or char == "_":
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j] == "_"):
                        j += 1
                    token = line[i:j]
                    if kw.isKeyword(token): 
                        self.txt2.insert(END, f'KW({token})\n') 
                    elif DataType.isDataType(token):
                        self.txt2.insert(END, f'TYPE({token})\n')
                    elif token.startswith('"'):
                        self.txt2.insert(END, f'STR({token})\n')
                    elif DataType.bool(token):
                        self.txt2.insert(END, f'BOOL({token})\n')
                    else: 
                        self.txt2.insert(END, f'ID({token})\n')
                    i = j
                elif char == '"':
                    #proceso para validar strings
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j] == '"' or line[j] == "_" or line[j].isspace()):
                        j += 1
                    token = line[i:j]
                    self.txt2.insert(END, f'STR({token})\n')
                    i = j
                elif char == "'":
                    #proceso para validar chars
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j] == "'"):
                        j += 1
                    token = line[i:j]
                    self.txt2.insert(END, f'CHAR({token})\n')
                    i = j
                elif char in ['+', '-', '*', '/', '%']:
                    self.txt2.insert(END, f'ARITHOP({char})\n')
                    i += 1
                elif char in ['=', '>', '<', '!', '&', '|']:
                    j = i + 2 if line[i+1] == '=' else i+ 1
                    token = line[i:j]
                    self.txt2.insert(END, f'LOGICOP({char})\n')
                    i = j
                elif char in [';', '(', ')', '{', '}', '[', ']', '.', ',']:
                    self.txt2.insert(END, f'DELIM({char})\n')
                    i += 1
                elif char.isspace():
                    i += 1
                else:
                    # No se encuentra token
                    i+=1
         
    
    def exit(self):
        sys.exit()
        
                    
analyzer = Analyzer()
