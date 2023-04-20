from libs.DataType import DataType
from libs.System import System
from libs.Keyword import Keyword
from libs.Operator import Operator
from tkinter import scrolledtext, END
class Core:
    
    def tokenize(code: str, txtbox: scrolledtext) -> list:
        tokens = []
        
        for line in code.split('\t'):
            words = line.split()
            kw = Keyword()
            op = Operator()
            for word in words:
                txtbox.insert(END, word + '\n')
                if kw.isKeyword(word) or DataType.isDataType(word):
                    print('{dt} keyword'.format(dt=word))
                elif op.isOperator(word):
                    print('{op} operator'.format(op=word))
                elif word.startswith("\"") and word.endswith("\"") and word.endswith(";"):
                    print('{st} string'.format(st=word))
                elif word.startswith("\'") and word.endswith("\'"):
                    print('{ch} char'.format(ch=word))
                else:
                    print('{id} ID'.format(id=word))
            
        
    
        return tokens
    
    def getTokenTypes(tokens: list) -> list:
        keywords = ["abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
                    "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "goto", 
                    "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", 
                    "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", 
                    "throws", "transient", "try", "void", "volatile", "while"]
        
        
        result = []
        
        for tk in tokens:
            if tk in keywords:
                result.append(("KEYWORD", tk))
            elif tk.isdigit() or tk.isnumeric() or tk.isdecimal() or DataType.float(tk):
                result.append(("NUMBER", tk))
            # elif tk in operators:
            #     if tk == ";":
            #         result.append(("ENDL", tk))
            #     else:
            #         result.append(("OPERATOR", tk))
            elif DataType.isDataType(tk) or DataType.bool(tk) or DataType.float(tk):
                result.append(("KEYWORD", tk))
            elif tk.startswith("\"") and tk.endswith("\""):
                result.append(("STRING", tk))
            elif tk.startswith("\'") and tk.endswith("\'"):
                result.append(("CHAR", tk))
            elif System.isJavaImport(tk):
                result.append(("IMPORT", tk))
            elif System.isSystemFunction(tk):
                result.append(("SYSFN", tk))
            else:
                result.append(("IDENTIFIER", tk))
        
        return result
        
    def group(tokens: list) :
        
        for t in tokens:
            print(t)
        
        