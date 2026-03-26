class ProcessController:
    def __init__(self):
        self.estado = "IDLE"  # IDLE, RUNNING, PAUSED
        self.stop_flag = False
    
    def iniciar(self):
        self.estado = "RUNNING"
        self.stop_flag = False
    
    def pausar(self):
        self.estado = "PAUSED"
    
    def reanudar(self):
        self.estado = "RUNNING"
    
    def detener(self):
        self.estado = "IDLE"
        self.stop_flag = True
    
    def esta_corriendo(self):
        return self.estado == "RUNNING"
    
    def esta_pausado(self):
        return self.estado == "PAUSED"
    
    def esta_detenido(self):
        return self.stop_flag
    
    def reset(self):
        self.stop_flag = False