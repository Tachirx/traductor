import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file = QFile("Interfaz/vista.ui") 
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"Error crítico: No se pudo abrir {ui_file.fileName()}")
            sys.exit(1)
        
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        self.setCentralWidget(self.ui.centralwidget)
        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.width(), self.ui.height())
        
        # Módulo A: Selección de idiomas e inversión
        self.selector_origen = self.ui.comboOrigen
        self.selector_destino = self.ui.comboDestino
        self.boton_invertir = self.ui.btnInvertir 

        # Módulo B: Paneles de texto y contadores
        self.caja_origen = self.ui.txtOrigen
        self.caja_destino = self.ui.txtDestino
        self.contador_caracteres = self.ui.lblContador 

        # Módulo C:  ejecucion
        self.radio_tradicional = self.ui.radioTradicional
        self.radio_tiempo_real = self.ui.radioTiempoReal 
        self.boton_traducir = self.ui.btnTraducir

        # Modulo D: UX e indicadores de carga
        self.indicador_estado = self.ui.lblEstado 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AppWindow()
    ventana.show()
    sys.exit(app.exec())