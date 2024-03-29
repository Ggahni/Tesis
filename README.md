# Deteccion de Cambios Archivo Web Venezuela (AWV)
Módulo de detección de cambios para el Archivo Web de Venezuela.

# Flaskapp

### [**app.py**](Flaskapp/app.py)
Archivo principal, es el que debe ser ejecutado para levantar la aplicación.

### [**changeDetector-backup.py**](Flaskapp/changeDetector-backup.py)
Versión estable previa almacenada por propósito de mantenimiento.

### [**changeDetector.py**](Flaskapp/changeDetector.py)
Versión actual del módulo de detección de cambios.

### [**util.py**](Flaskapp/util.py)
Módulo que permite la captura completa del sitio web en lugar de sólo la visualizada en el rendering original.

### [**\_\_pycache\_\_**](Flaskapp/__pycache__)
Elementos de uso general de Python.

### [static](Flaskapp/static)
Imágenes producidas luego de la ejecución de la detección de cambios, se mantienen por interés general, sirven como ejemplo.
Se usan al momento del rendering de **_resultados.html_** de la siguiente manera:
  - **awv_logo.png**: logo del Archivo Web Venezuela
  - **block_text_change_percentage.png**: gráfico de barras que muestra el % de cambios por cada uno de los bloques de texto.
  - **new_screenshot.png**: captura de pantalla de la versión que se está revisando del sitio web.
  - **old_screenshot.png**: captura de pantalla de la versión almacenada contra la que se comparará para la detección de cambios.

### [templates](Flaskapp/templates)
Código de los sitios web que conforman parte de la aplicación, de la siguiente manera:
  - **index.html**: interfaz principal de la aplicación, aquí se colocan los URL/ruta física de los sitios web a comparar.
  - **new_site.html**: sitio web que se está comparando (versión actualizada) que se reconstruye y al que se le agrega un borde a los bloques que han sufrido algún cambio para facilitar la visualización de éstos.
  - **resultados.html**: interfaz de resultados de la detección de cambios, muestra las imágenes contenidas en el directorio **_static_**.

# Desarrolladores
Luis R. Aguiar C. \(**@Ggahni**\)
