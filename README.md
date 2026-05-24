# Traductor Multilingüe de Escritorio - UNEFA

Aplicación de escritorio nativa desarrollada con **PySide6** orientada a la comunicación global, que soporta traducción por procedimiento y en tiempo real con control estricto asíncrono y excelente interfaz visual (Tema oscuro/Premium).

## Requisitos Previos
* Python 3.9 o superior instalado.
* Conexión a internet activa para el consumo de la API de traducción.

## Instalación y Ejecución

1. **Clonar o descargar el repositorio**
2. **Crear un Entorno Virtual** (Recomendado):
   ```bash
   python -m venv .venv
   ```
3. **Activar el Entorno Virtual**:
   * En Windows:
     ```bash
     .venv\Scripts\activate
     ```
   * En macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
4. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Ejecutar la Aplicación**:
   ```bash
   python main.py
   ```

## Módulos y Arquitectura
* **Eventos (`Eventos/`)**: Hilos concurrentes (`QThread`) y Gestor de temporizadores (Debounce) para traducciones en tiempo real sin congelamiento de UI.
* **Motor (`Motor/`)**: Integración con `deep-translator` mapeando códigos exactos de idioma y control estricto de excepciones de conectividad.
* **Vista (`Vista/`)**: Interfaz premium con layouts simétricos, barra de herramientas interactiva y hoja de estilos QSS, conectada dinámicamente mediante `QUiLoader`.
* **Controlador (`main.py`)**: Núcleo orquestador que inyecta dependencias e inicializa el bucle de la aplicación nativa.
