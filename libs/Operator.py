import operator
class Operator:
    
    operators = ["=", "+", "-", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "&&", "||", "!", "&", "|", "^",
                 "~", "<<", ">>", ">>>", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", ">>>=", "&=", "^=", "|=", 
                 "++", "--", ".", ",", ";", "(", ")", "[", "]", "{", "}"]
    
    def isOperator(self, w: str) -> bool:
        return w in self.operators