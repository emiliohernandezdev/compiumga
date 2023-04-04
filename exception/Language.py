class LanguageException(Exception):
    """Excepción definida por Emilio Hernandez para obtener errores que pueden existir en el codigo fuente

    Attributes:
        line -- linea de codigo a validar
    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, word: str, message=f"Invalid syntax"):
        self.message = message
        super().__init__(self.message)