class Validators:
    @staticmethod
    def validar_delay(delay):
        '''Valida el delay entre envíos'''
        try:
            delay = float(delay)
            return 5 <= delay <= 60, delay
        except ValueError:
            return False, None
    
    @staticmethod
    def validar_fontsize(fontsize):
        '''Valida el tamaño de fuente'''
        try:
            fontsize = int(fontsize)
            return 8 <= fontsize <= 24, fontsize
        except ValueError:
            return False, None
    
    @staticmethod
    def validar_columnas_unicas(columnas):
        '''Valida que no haya columnas duplicadas'''
        return len(columnas) == len(set(columnas))