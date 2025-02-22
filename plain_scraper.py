import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from aux_methods import *

def download_images_new_format(base_url, output_base, min_range=1, max_range=10000):
    """Descarga imágenes de páginas individuales con formato http://base_url/p1 o http://base_url/p-1."""
    output_folder = os.path.join(output_base, "images")
    os.makedirs(output_folder, exist_ok=True)
    
    for i in range(min_range, max_range + 1):
        for suffix in [f"p{i}", f"p-{i}", f"p{i}-2", f"p-{i}-2"]:
            print(suffix)
            image_page_url = urljoin(base_url, suffix)
            response = requests.get(image_page_url)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            image_container = soup.find(class_="comic-table")
            if not image_container:
                continue
            
            img_tag = image_container.find('img')
            if not img_tag or not img_tag.get('src'):
                continue
            
            img_url = urljoin(image_page_url, img_tag['src'])
            # Usar el sufijo como nombre del archivo
            img_name = sanitize_filename(suffix + ".png")
            
            img_data = requests.get(img_url).content
            img_path = os.path.join(output_folder, img_name)
            with open(img_path, 'wb') as f:
                f.write(img_data)
                print(f"Descargada: {img_name}")

# Uso del script
url = "www.example.com"  # Reemplaza con la URL real
carpeta_destino = "descargas"
min_range = 1092
max_range = 1273
# regex_filtro = r"^p\-\d{1,4}\.png$"  # Expresión regular para imágenes que empiezan con 'p', siguen con hasta 4 dígitos y terminan en .png
download_images_new_format(url, carpeta_destino, min_range, max_range)
