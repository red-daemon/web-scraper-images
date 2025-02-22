# Web Scraper Images

Este es un programa en Python para descargar imágenes de páginas web que publican imágenes periódicamente. El script permite extraer imágenes de dos formatos distintos de página y organizarlas en carpetas según su estructura.

## Características
- Descarga imágenes desde una página de archivos organizadas en capítulos.
- Permite definir una expresión regular para filtrar las imágenes descargadas.
- Maneja páginas donde las imágenes están en páginas individuales con un patrón de URL predecible.
- Guarda las imágenes en carpetas organizadas por capítulos o en una única carpeta según el formato.

## Requisitos

- Python 3.7+
- `requests`
- `beautifulsoup4`

Puedes instalar las dependencias ejecutando:

```bash
pip install requests beautifulsoup4
```

## Uso

### Descarga de imágenes organizadas en capítulos

Ejemplo de uso:

```python
from scraper import download_images

url = "https://example.com"
folder = "archive"
carpeta_destino = "descargas"
regex_filtro = r"^p\d{1,4}\.png$"

download_images(url, folder, carpeta_destino, regex_filtro)
```

### Descarga de imágenes desde páginas individuales

Ejemplo de uso:

```python
from scraper import download_images_new_format

url = "https://example.com"
carpeta_destino = "descargas"
regex_filtro = r"^p\d{1,4}\.png$"

download_images_new_format(url, carpeta_destino, regex_filtro)
```

## Estructura de Archivos Descargados

Para el formato basado en capítulos:
```
/descargas/
    /archive/
        /Capítulo 1/
            imagen1.png
            imagen2.png
        /Capítulo 2/
            imagen3.png
            imagen4.png
```

Para el formato basado en páginas individuales:
```
/descargas/
    /images/
        p1.png
        p2.png
        p3.png
```

## Notas
- Asegúrate de proporcionar una URL válida.
- Si las imágenes no se descargan, verifica si la estructura de la página ha cambiado.
- El script reemplaza caracteres inválidos en los nombres de archivos y carpetas.

## Licencia
Este proyecto está bajo la licencia MIT.

