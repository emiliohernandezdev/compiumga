import operator
class Operator:
    
    operators = ["=", "+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "&&", "||", "!", "&", "|", "^",
                 "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", ">>>=", "&=", "^=", "|=", 
                 "++", "--", ".", ",", ";", "(", ")", "[", "]", "{", "}"]
    
    aritmethics = ['+', '-', '*', '/', '%'];
    logics = ['=', '>', '<', '!', '&', '|'];
    delimiters = [';', '(', ')', '{', '}', '[', ']', '.', ','];
    
    def isOperator(self, w: str) -> bool:
        return w in self.operators
    
    
    def validateOperator(self, op: str) -> bool:
        if op in self.aritmethics or op in self.logics or op in self.delimiters: return True
        else: return False

    def getType(self, op: str) -> str:
        if op in self.aritmethics:
            return "arithmetic"
        elif op in self.logics:
            return "logic"
        elif op in self.delimiters:
            return "delimiter"
        else:
            return None
        
        
    