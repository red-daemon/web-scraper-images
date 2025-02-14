import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(base_url, folder, output_base, regex_pattern):
    """Descarga imágenes desde una página de archivos, organizándolas en carpetas por capítulos."""
    # Crear la carpeta base de salida
    output_folder = os.path.join(output_base, folder)
    os.makedirs(output_folder, exist_ok=True)
    
    # Construir la URL de la página del archivo
    archive_url = urljoin(base_url, folder)
    
    # Obtener el contenido de la página
    response = requests.get(archive_url)
    if response.status_code != 200:
        print(f"Error al acceder a {archive_url}")
        return
    
    # Analizar el HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Compilar la expresión regular
    pattern = re.compile(regex_pattern)
    
    # Buscar la sección de contenido principal
    content_section = soup.find(class_="entry-content")
    if not content_section:
        print("No se encontró la sección de contenido principal.")
        return
    
    # Buscar los capítulos
    chapters = content_section.find_all(class_="comic-archive-chapter-wrap")
    
    for chapter in chapters:
        chapter_title_tag = chapter.find(class_="comic-archive-chapter")
        if not chapter_title_tag:
            continue
        
        chapter_title = chapter_title_tag.text.strip()
        chapter_folder = os.path.join(output_folder, chapter_title)
        os.makedirs(chapter_folder, exist_ok=True)
        
        # Buscar imágenes dentro del capítulo
        image_list = chapter.find(class_="comic-archive-list-wrap")
        if not image_list:
            continue
        
        for entry in image_list.find_all('li'):
            title_tag = entry.find(class_="comic-archive-title")
            if not title_tag:
                continue
            
            link = title_tag.find('a', href=True)
            if not link:
                continue
            
            # Obtener la URL de la página de la imagen
            image_page_url = urljoin(archive_url, link['href'])
            
            # Obtener la imagen desde la página de destino
            image_page_response = requests.get(image_page_url)
            if image_page_response.status_code != 200:
                print(f"Error al acceder a la página de la imagen: {image_page_url}")
                continue
            
            image_soup = BeautifulSoup(image_page_response.text, 'html.parser')
            image_container = image_soup.find(class_="comic")
            if not image_container:
                print("No se encontró la imagen en la página.")
                continue
            
            img_tag = image_container.find('img')
            if not img_tag or not img_tag.get('src'):
                print("No se encontró una imagen válida.")
                continue
            
            img_url = urljoin(image_page_url, img_tag['src'])
            img_name = os.path.basename(img_url)
            
            # Filtrar por expresión regular
            if not pattern.match(img_name):
                continue
            
            # Descargar la imagen
            img_data = requests.get(img_url).content
            
            # Guardar la imagen en la carpeta del capítulo
            img_path = os.path.join(chapter_folder, img_name)
            with open(img_path, 'wb') as f:
                f.write(img_data)
                print(f"Descargada: {img_name} en {chapter_title}")

# Uso del script
url = ""  # Reemplaza con la URL real
folder = "archive"
carpeta_destino = "descargas"
regex_filtro = r"^p\d{1,4}\.png$"  # Expresión regular para imágenes que cumplen el criterio
download_images(url, folder, carpeta_destino, regex_filtro)
