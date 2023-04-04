import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import END, scrolledtext as st
from libs.Core import Core

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
        
        self.txt1.delete('1.0', END);
        self.txt2.delete('1.0', END);
        self.txt3.delete('1.0', END);

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
    
        #Llamar a la funcion para tokenizar
        tokens = Core.tokenize(lines)
        
        types = Core.getTokenTypes(tokens)
        
        self.clasify(types)
        
        
         
    
    def exit(self):
        sys.exit()
        
    
    def clasify(self, types: list):
        
        for t in types:
            match t[0]:
                case "KEYWORD":
                    self.txt2.insert(END, "KW({kw}) ".format(kw=t[1]))
                case "ENDL":
                    self.txt2.insert(END, "ENDL(;)\n\n")
                case "IDENTIFIER":
                    self.txt2.insert(END, "ID({id}) ".format(id=t[1]))
                case "OPERATOR":
                    if t[1] == "{" or t[1] == "}":
                        self.txt2.insert(END, "OP({op})\n ".format(op=t[1]))
                    else:
                        self.txt2.insert(END, "OP({op}) ".format(op=t[1]))
                case "NUMBER":
                    self.txt2.insert(END, "NUM({n}) ".format(n=t[1]))
                case "STRING":
                    self.txt2.insert(END, "STR({s}) ".format(s=t[1]))
                case "CHAR":
                    self.txt2.insert(END, "CHAR({s}) ".format(s=t[1]))
                case "SYSFN":
                    self.txt2.insert(END, "SYSFN({s}) ".format(s=t[1]))
                case "IMPORT":
                    self.txt2.insert(END, "IMPORTPKG({i}) ".format(i=t[1]))
                    
analyzer = Analyzer()
