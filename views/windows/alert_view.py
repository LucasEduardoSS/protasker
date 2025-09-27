from customtkinter import CTkToplevel

from utils.gui_utils import center_window
from views.components.pro_widgets import ProButton, ProLabel


class AlertView(CTkToplevel):
    def __init__(self, master, title, message, **kwargs):
        super().__init__(master, **kwargs)

        self.title(title)
        self.configure(fg_color="#2E333C", bg_color="#2C2E33")

        # Centraliza a janela
        center_window(self, (320, 90))

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        self.message_label = ProLabel(self, text=message)
        self.message_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 10))

        self.confirm_button = ProButton(self, text="OK", command=None)
        self.confirm_button.grid(row=1, column=0, padx=10, pady=10)

        self.cancel_button = ProButton(self, text="Cancelar", command=None)
        self.cancel_button.grid(row=1, column=1, padx=10, pady=10)
