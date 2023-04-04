class System:
    
    def isJavaImport(t: str) -> bool:
        return t.startswith("java.")
    
    def isSystemFunction(s: str) -> bool:
        return s.startswith("System.")