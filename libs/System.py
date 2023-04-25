class System:
    
    def isScope(s: str):
        return s in ["public", "private", "protected"];

    def isDirective(s: str):
        return s in ["readonly", "static", "final"]
    
    