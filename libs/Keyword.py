import keyword
class Keyword:
    keywords = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const',
                'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 
                'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 
                'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 
                'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 
                'try', 'void', 'volatile', 'while']

    
    def isKeyword(self, kw: str) -> bool:
        return kw in self.keywords or  kw in keyword.kwlist