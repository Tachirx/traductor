import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Módulos del Backend y Eventos
from Motor.motor_traduccion import MotorTraduccion
from Eventos.concurrencia import HiloTraductor
from Eventos.gestor_eventos import GestorEventos

# Módulo Frontend del Compañero (Original)
from Interfaz.main import AppWindow

class ControladorTraductor:
    def __init__(self):
        self.motor = MotorTraduccion()
        self.gestor_eventos = GestorEventos()
        self.hilo_traductor = HiloTraductor(self.motor)
        
        # Instanciar la Vista original del compañero
        self.vista = AppWindow()
        self.modo_actual = "manual"
        
        self.mapa_idiomas = {
            "Detectar automáticamente": "auto",
            "Español": "es",
            "Inglés": "en",
            "Portugués": "pt",
            "Francés": "fr",
            "Italiano": "it"
        }
        
        self.configurar_conexiones()
        
        # Configuración inicial de la UI que no está en su archivo pero es necesaria para UX
        self.vista.caja_destino.setReadOnly(True)
        self.vista.radio_tradicional.setChecked(True)
        self.vista.indicador_estado.setText("Listo")
        
        # Temporizador para el texto parpadeante (Requisito de Iliane)
        self.timer_parpadeo = QTimer()
        self.timer_parpadeo.setInterval(500)
        self.timer_parpadeo.timeout.connect(self.alternar_texto_parpadeo)
        self.estado_parpadeo = False

    def configurar_conexiones(self):
        self.vista.boton_invertir.clicked.connect(self.intercambiar_idiomas)
        self.vista.boton_traducir.clicked.connect(self.solicitar_traduccion_manual)
        
        self.vista.radio_tradicional.clicked.connect(lambda: self.cambiar_modo("manual"))
        self.vista.radio_tiempo_real.clicked.connect(lambda: self.cambiar_modo("tiempo_real"))
        
        self.vista.caja_origen.textChanged.connect(self.al_cambiar_texto)
        self.gestor_eventos.solicitud_ejecucion.connect(self.ejecutar_traduccion_asincrona)
        
        # Señales del hilo
        self.hilo_traductor.inicio_carga.connect(self.bloquear_interfaz)
        self.hilo_traductor.resultado_listo.connect(self.mostrar_resultado)
        self.hilo_traductor.error_ocurrido.connect(self.mostrar_error)
        self.hilo_traductor.fin_carga.connect(self.desbloquear_interfaz)

    def cambiar_modo(self, modo):
        self.modo_actual = modo
        if modo == "manual":
            self.vista.boton_traducir.setEnabled(True)
        else:
            self.vista.boton_traducir.setEnabled(False)

    def al_cambiar_texto(self):
        texto = self.vista.caja_origen.toPlainText()
        self.vista.contador_caracteres.setText(f"Caracteres: {len(texto)}")
        
        if self.modo_actual == "tiempo_real" and texto.strip():
            self.gestor_eventos.al_cambiar_texto()

    def solicitar_traduccion_manual(self):
        if self.modo_actual == "manual":
            self.ejecutar_traduccion_asincrona()

    def intercambiar_idiomas(self):
        origen_actual = self.vista.selector_origen.currentText()
        destino_actual = self.vista.selector_destino.currentText()
        
        if origen_actual == "Detectar automáticamente":
            self.mostrar_error("No se puede intercambiar cuando el origen es 'Detectar automáticamente'.")
            return
            
        self.vista.selector_origen.setCurrentText(destino_actual)
        self.vista.selector_destino.setCurrentText(origen_actual)
        
        if self.vista.caja_origen.toPlainText().strip() and self.modo_actual == "tiempo_real":
            self.ejecutar_traduccion_asincrona()

    def ejecutar_traduccion_asincrona(self):
        texto = self.vista.caja_origen.toPlainText()
        
        if not texto.strip():
            self.vista.caja_destino.setPlainText("")
            return
            
        origen_legible = self.vista.selector_origen.currentText()
        destino_legible = self.vista.selector_destino.currentText()
        
        codigo_origen = self.mapa_idiomas.get(origen_legible, "auto")
        codigo_destino = self.mapa_idiomas.get(destino_legible, "es")
        
        if codigo_origen == codigo_destino:
            self.vista.caja_destino.setPlainText(texto)
            return

        if self.hilo_traductor.isRunning():
            self.hilo_traductor.wait()
            
        self.hilo_traductor.configurar(texto, codigo_origen, codigo_destino)
        self.hilo_traductor.start()

    def alternar_texto_parpadeo(self):
        self.estado_parpadeo = not self.estado_parpadeo
        if self.estado_parpadeo:
            self.vista.indicador_estado.setText("Traduciendo... ⏳")
        else:
            self.vista.indicador_estado.setText("Traduciendo...   ")

    def bloquear_interfaz(self):
        self.vista.caja_origen.setEnabled(False)
        self.vista.boton_traducir.setEnabled(False)
        self.vista.boton_invertir.setEnabled(False)
        self.timer_parpadeo.start()
        self.alternar_texto_parpadeo()

    def desbloquear_interfaz(self):
        self.timer_parpadeo.stop()
        self.vista.caja_origen.setEnabled(True)
        self.vista.boton_invertir.setEnabled(True)
        if self.modo_actual == "manual":
            self.vista.boton_traducir.setEnabled(True)
        self.vista.indicador_estado.setText("Listo")

    def mostrar_resultado(self, texto):
        self.vista.caja_destino.setPlainText(texto)

    def mostrar_error(self, error):
        from PySide6.QtWidgets import QMessageBox
        self.timer_parpadeo.stop()
        self.vista.caja_destino.setPlainText(f"Error: {error}")
        QMessageBox.critical(self.vista, "Fallo de Red / Sistema", error)

    def iniciar(self):
        self.vista.show()

def main():
    app = QApplication(sys.argv)
    controlador = ControladorTraductor()
    controlador.iniciar()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
