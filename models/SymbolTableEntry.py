class SymbolTableEntry:
    
    def __init__(self, name='', type='', initvalue='', scope=''):
        self.name = name
        self.type = type
        self.initvalue = initvalue
        self.scope = scope
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def getType(self):
        return self.type
    
    def setType(self, type):
        self.type = type
        
    def getInitValue(self):
        return self.initvalue
    
    def setInitValue(self, value):
        self.initvalue = value
    
    def getScope(self):
        return self.scope
    
    def setScope(self, scope):
        self.scope = scope