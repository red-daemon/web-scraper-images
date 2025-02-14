import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(base_url, output_folder):
    """Descarga todas las imágenes de una página web y las guarda en una carpeta."""
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Obtener el contenido de la página
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Error al acceder a {base_url}")
        return
    
    # Analizar el HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    
    for img in images:
        img_url = img.get('src')
        if not img_url:
            continue
        
        # Convertir URL relativa a absoluta
        img_url = urljoin(base_url, img_url)
        
        # Obtener el nombre del archivo
        img_name = os.path.basename(img_url)
        
        # Descargar la imagen
        img_data = requests.get(img_url).content
        
        # Guardar la imagen
        img_path = os.path.join(output_folder, img_name)
        with open(img_path, 'wb') as f:
            f.write(img_data)
            print(f"Descargada: {img_name}")

# Uso del script
url = "http://page.com/"  # Reemplaza con la URL real
carpeta_destino = "imagenes_descargadas"
download_images(url, carpeta_destino)
