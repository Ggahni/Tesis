# Deteccion de Cambios AWV

# Flaskapp

### **\_\_app.py\_\_**
Archivo principal, es el que debe ser ejecutado para levantar la aplicación

### **changeDetector-backup.py**
Versión estable previa almacenada por propósito de mantenimiento

### **changeDetector.py**
Versión actual del módulo de detección de cambios.

### **util.py**
Módulo que permite la captura completa del sitio web en lugar de sólo la visualizada en el rendering original.

### pycache
Elementos de uso general de Python

### static
Imágenes producidas luego de la ejecución de la detección de cambios, se mantienen por interés general, sirven como ejemplo.
Se usan al momento del rendering de **_resultados.html_** de la siguiente manera:
  1. **block_text_change_percentage.png**: gráfico de barras que muestra el % de cambios por cada uno de los bloques de texto.
  2. **new_screenshot.png**: captura de pantalla de la versión que se está revisando del sitio web.
  3. **old_screenshot.png**: captura de pantalla de la versión almacenada contra la que se comparará para la detección de cambios.

### templates
Código de los sitios web que conforman parte de la aplicación, de la siguiente manera:
  1. **index.html**: interfaz principal de la aplicación, aquí se colocan los URL/ruta física de los sitios web a comparar.
  2. **new_site.html**: sitio web que se está comparando (versión actualizada) que se reconstruye y al que se le agrega un borde a los bloques que han sufrido algún cambio para facilitar la visualización de éstos.
  3. **resultados.html**: interfaz de resultados de la detección de cambios, muestra las imágenes contenidas en el directorio **_static_**.
