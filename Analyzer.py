import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import END, scrolledtext as st
from libs.Core import Core
from libs.Keyword import Keyword
from libs.Operator import Operator
from libs.DataType import DataType
from libs.System import System
from models.SymbolTableEntry import SymbolTableEntry
from views.SymbolTable import SymbolTableView
from tkinter import *
import string
class Analyzer():
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
        self.ids = list()
        
    def show(self):
        self.window.mainloop()
        
    def setTitle(self):
        self.window.title("Compiladores / Emilio Hernández")
        
    def cleanFileAndPath(self):
        self.currentFile = None
        self.currentPath = ''
        
    def buildGrid(self):

        self.txt1 = st.ScrolledText(self.window, width=45, height=25)
        self.txt1.grid(column=0, row=0, padx=5, pady=5)
        self.txt1.delete('1.0', END)

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

    variables = []                
                
    def businessProcess(self):
        self.txt2.delete(1.0, END)
        self.txt3.delete(1.0, END)
        lines = self.txt1.get('1.0', END).strip()

        kw = Keyword()
        op = Operator()
        child = SymbolTableView()
        self.variables = []

        for numberLine, line in enumerate(lines.split('\n'), 1):
            ste = SymbolTableEntry()
            i = 0
            line = line.strip()
            # self.validateLine(line)
            while i < len(line):
                char = line[i]
                if char.isdigit():
                    j = i + 1
                    while j < len(line) and (line[j].isdigit() or line[j].isnumeric() or line[j] == "."):
                        j += 1
                    token = line[i:j]
                    self.txt2.insert(END, f'NUM({token})\n')
                    try:
                        val = int(token)
                        ste.setInitValue(val)
                    except:
                        try:
                            val = float(token)
                            ste.setInitValue(val)
                        except:
                            self.txt3.insert(END, f"ERROR: Numero '{token}' no valido. Linea {numberLine}\n")
                    finally: 
                        ste.setInitValue(val)
                    i = j
                elif char.isalpha() or char.isalnum() or char in string.punctuation and char not in ['"', "'"]:
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j] == "_" ):
                        j += 1
                    token = line[i:j]
                    
                    if kw.isKeyword(token): 
                        self.txt2.insert(END, f'KW({token})\n')
                        if DataType.isDataType(token):
                            ste.setType(token)
                    elif DataType.isDataType(token):
                        self.txt2.insert(END, f'TYPE({token})\n')
                        ste.setType(token)
                    elif token.startswith('"'):
                        self.txt2.insert(END, f'STR({token})\n')
                    elif DataType.bool(token):
                        self.txt2.insert(END, f'BOOL({token})\n')
                        ste.setInitValue(token)
                    elif token.isidentifier():
                        lnSplt = line.split()
                        if System.isScope(lnSplt[0]) or DataType.isDataType(lnSplt[0]):
                            if token not in self.variables:
                                self.txt2.insert(END, f'ID({token})\n')
                                ste.setName(token)
                                self.variables.append(token)
                            else:
                                self.txt3.insert(END, f"ERROR: Identificador de variable '{token}' duplicado. Linea {numberLine}\n")
                        else:
                            if lnSplt[0] not in self.variables:
                                self.txt3.insert(END, f"ERROR: Referencia a objeto '{token}' no declarado. Linea {numberLine}\n")
                            else:
                                ste.setName(lnSplt[0])
                    elif op.validateOperator(char):
                        opType = op.getType(char)
                        match opType:
                            case 'arithmetic':
                                self.txt2.insert(END, f'ARITHOP({char})\n')
                                i += 1
                            case 'logic':
                                j = i + 2 if line[i+1] == '=' else i+ 1
                                token = line[i:j]
                                self.txt2.insert(END, f'LOGICOP({char})\n')
                                i = j
                            case 'delimiter':
                                self.txt2.insert(END, f'DELIM({char})\n')
                                i += 1
                    else:
                        self.txt3.insert(END, f"ERROR: Identificador '{token}' no valido. Linea {numberLine}\n")
                    i = j
                    
                elif char == '"':
                    #proceso para validar strings
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j] == '"' or line[j] == "_" or line[j].isspace() or not line[j] in string.punctuation):
                        j += 1
                    token = line[i:j]
                    self.txt2.insert(END, f'STR({token})\n')
                    ste.setInitValue(token)
                    i = j
                elif char == "'":
                    #proceso para validar chars
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j] == "'"):
                        j += 1
                    token = line[i:j]
                    self.txt2.insert(END, f'CHAR({token})\n')
                    ste.setInitValue(token)
                    i = j
                
                elif char.isspace():
                    i += 1
                else:
                    # No se encuentra token
                    i+=1
                    
            if line:
                self.getNameTypeAndScope(line, numberLine, ste)
                child.insertEntry(ste)
                
                    
    def getNameTypeAndScope(self, line: str, lnNumber: int, ste: SymbolTableEntry):
        if line:
            lnArr = line.strip().split()
            typeOrScope = lnArr[0]
            kw = Keyword()
            #si viene nivel de acceso
            
            if System.isScope(typeOrScope):
                match typeOrScope:
                    case 'public':
                        ste.setScope('0')
                    case 'private':
                        ste.setScope('1')
                    case 'protected':
                        ste.setScope('2')
                    case _:
                        ste.setScope('0')
                nextToken = lnArr[1]
                if DataType.isDataType(nextToken) or nextToken == "void":
                    nextToken = lnArr[2].strip()
                    if System.isFunction(nextToken):
                        ste.setType('function')
                        ste.setName(nextToken[0:nextToken.index(")") + 1])
                    else:
                        validation = self.validateTypeAndValue(lnArr[1], ste.getInitValue())
                        if validation == True:
                            ste.setType(lnArr[1])
                            ste.setName(lnArr[2])
                        else:
                            self.txt3.insert(END, f"ERROR: El valor asignado no es del tipo de la variable '{ste.getName()}', esperaba un tipo: '{ste.getType()}'. Linea {lnNumber}\n")
                elif System.isDirective(nextToken):
                    ste.setName(lnArr[4])
                elif kw.isKeyword(nextToken) and nextToken == "class":
                    ste.setType(nextToken)
                    if "{" in lnArr[2]:
                        name = lnArr[2]
                        ste.setName(name[0:name.index("{")])
                    else:
                        try:
                            name = lnArr[2]
                            delims = lnArr[3]
                            
                            if "{}" not in name:
                                ste.setName(name)
                        except:
                            return None
            #si viene tipo de dato
            elif DataType.isDataType(typeOrScope):
                ste.setScope('0')
                validation = self.validateTypeAndValue(typeOrScope, ste.getInitValue())
                if validation == True:
                    ste.setType(typeOrScope)
                    ste.setName(lnArr[1])
                else:
                    self.txt3.insert(END, f"ERROR: El valor asignado no es del tipo de la variable '{ste.getName()}', esperaba un tipo: '{ste.getType()}'. Linea {lnNumber}\n")
            elif typeOrScope in string.punctuation:
                pass
            elif not typeOrScope.isalnum():
                if typeOrScope in self.variables:
                    ste.setName(typeOrScope)
                    # ste.setInitValue()
                self.txt3.insert(END, f"ERROR: Caracter ilegal {typeOrScope} en la linea {lnNumber}\n")
        
        
    def validateTypeAndValue(self, type: str, value: str):
        match type:
            case 'int':
                if isinstance(value, int): return True
                else: return False
            case 'float':
                if isinstance(value, float): return True
                else: return False
            case 'double':
                if isinstance(value, float): return True
                else: return False
            case 'String':
                if isinstance(value, str): return True
                else: return False
            case 'char':
                if isinstance(value, str): return True
                else: return False
            case 'boolean':
                if DataType.bool(value): return True
                else: return False
            case 'byte':
                if isinstance(value, int): return True
                else: return False
    
    def exit(self):
        sys.exit()
        
                    
if __name__ == "__main__":
    an = Analyzer()
    an.show()