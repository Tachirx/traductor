from PySide6.QtCore import QObject, Signal, QTimer

class GestorEventos(QObject):
    solicitud_ejecucion = Signal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
       
        self.timer.setInterval(700) 
        self.timer.timeout.connect(self.solicitud_ejecucion.emit)

    def al_cambiar_texto(self):
       
        self.timer.stop()
        self.timer.start()