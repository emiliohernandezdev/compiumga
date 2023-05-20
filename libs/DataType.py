import ast
from tkinter import END
from tkinter.scrolledtext import ScrolledText
from models.SymbolTableEntry import SymbolTableEntry 
from libs.System import System

class DataType:
    

    
    def isDataType(type: str) -> bool:
        primitives = ["byte", "short", "int", "long", "float", "double", "boolean", "char"]
        nonprimitive = ["String", "ArrayList"]
        joins = (primitives + nonprimitive)
        
        result = []
        
        for p in joins:
            result.append(f"{p}[]")
            
        result = (joins + result)
        
        return type in result

    def float(n: str) -> bool:
        try:
            float(n)
            return True
        except:
            return False
        
    def bool(b: str) -> bool:
        if b.lower() in ["true", "false"]:
            convert = b[0].upper()
            final = convert + b[1:]
            try:
                bool(final)
                return True
            except:
                return False
        else:
            return False
        
    def dataTypeSymbolTable(line: str, txt: ScrolledText, ste: SymbolTableEntry) -> SymbolTableEntry:
        print(f'line: {line}')
        tkSplit = line.split()
        token = tkSplit[0]
        if System.isScope(token):
            print('scope')
            match token:
                case 'public':
                    ste.setScope('1')
                case 'private':
                    ste.setScope('2')
                case 'protected':
                    ste.setScope('3')
                case _:
                    ste.setScope('1')
            ste.setType(tkSplit[1])
        elif DataType.isDataType(token):
            print('datatype')
            match token:
                case 'byte':
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType('byte')
                case 'int':
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType('int')
                case 'float':
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType('float')
                case 'long':
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType('long')
                case 'short':
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType('short')
                case 'double':
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType('double')
                case _:
                    txt.insert(END, f'NUM({token})\n')
                    ste.setType(token)
            ste.setScope('1')
        return ste
        
            