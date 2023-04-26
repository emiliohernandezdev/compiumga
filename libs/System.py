class System:
    
    def isScope(s: str):
        return s in ["public", "private", "protected"];

    def isDirective(s: str):
        return s in ["readonly", "static", "final"]
    
    def isFunction(t: str) -> bool:
        if "(" in t and ")" in t and "{" in t:
            return True
        else:
            return False
    
    