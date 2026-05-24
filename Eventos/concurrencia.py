from PySide6.QtCore import QThread, Signal

class HiloTraductor(QThread):
    resultado_listo = Signal(str)
    error_ocurrido = Signal(str)
    inicio_carga = Signal()
    fin_carga = Signal()

    def __init__(self, motor):
        super().__init__()
        self.motor = motor
        self.texto = ""
        self.origen = ""
        self.destino = ""

    def configurar(self, texto, origen, destino):
        self.texto = texto
        self.origen = origen
        self.destino = destino

    def run(self):
        if not self.texto or not self.texto.strip():
            return
        
        self.inicio_carga.emit()
        try:
            resultado = self.motor.traducir(self.texto, self.origen, self.destino)
            self.resultado_listo.emit(resultado)
        except Exception as e:
           
            self.error_ocurrido.emit(str(e))
        finally:
            self.fin_carga.emit()