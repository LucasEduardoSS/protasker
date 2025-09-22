from customtkinter import CTkImage
from pathlib import Path
from PIL import Image

# Obtém o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Define o caminho para a pasta de imagens
IMAGES_DIR = BASE_DIR / "images"


def get_image_path(image_name):
    """ Retorna o caminho completo para a imagem. """
    return str(IMAGES_DIR / image_name)

def get_image(image_name):
    """ Retorna uma imagem. """
    return Image.open(get_image_path(image_name))

def get_image_as_tkimage(image_name, size=None):
    """ Retorna a imagem como CTkImage. """
    return CTkImage(
        light_image=get_image(image_name),
        dark_image=get_image(image_name),
        size=(size, size) if size else None
    )
