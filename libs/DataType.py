import ast 

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
        if b in ["true", "false"]:
            convert = b[0].upper()
            final = convert + b[1:]
            try:
                bool(final)
                return True
            except:
                return False
        else:
            return False
        
        
            