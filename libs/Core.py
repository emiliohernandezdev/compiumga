from libs.DataType import DataType
from libs.System import System

class Core:
    
    def tokenize(code: str) -> list:
        
        delimiters = [" ", "\t", "\n", "/", "(", ")", "{", "}", ";", ",", "+", ".*", "-", "*", "=", "<", ">", "&", "|", "?", ":", "%", "~", "^"]
        tokens = []
        current_token = ""

        
        for character in code:
            if character in delimiters:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                if character.strip():
                    tokens.append(character)
            else:
                current_token += character  
    
        return tokens
    
    def getTokenTypes(tokens: list) -> list:
        keywords = ["abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue",
                    "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "goto", 
                    "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", 
                    "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", 
                    "throws", "transient", "try", "void", "volatile", "while"]
        operators = ["=", "+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", ">>>=", "&=", "^=", "|=", "++", "--", ".", ",", ";", "(", ")", "[", "]", "{", "}"]
        
        result = []
        
        for tk in tokens:
            if tk in keywords:
                result.append(("KEYWORD", tk))
            elif tk.isdigit() or tk.isnumeric() or tk.isdecimal() or DataType.float(tk):
                result.append(("NUMBER", tk))
            elif tk in operators:
                if tk == ";":
                    result.append(("ENDL", tk))
                else:
                    result.append(("OPERATOR", tk))
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
        
        