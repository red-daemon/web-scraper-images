import re

def sanitize_filename(filename):
    """Elimina caracteres inválidos para nombres de archivos y carpetas en Windows y otros sistemas operativos."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)