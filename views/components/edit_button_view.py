from customtkinter import CTkImage, CTkButton
from PIL import Image

IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"

edit_icon = CTkImage(
    light_image=Image.open(IMAGES_PATH + "edit-icon.png"),
    dark_image=Image.open(IMAGES_PATH + "edit-icon.png"),
    size=(20, 20)
)

class EditButton(CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            width=30,
            height=20,
            font=("Tahoma", 11),
            image=edit_icon,
            fg_color="transparent",
            hover_color="#3E4D66",
            command = self._command
        )
