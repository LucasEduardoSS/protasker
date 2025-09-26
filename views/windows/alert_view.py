from customtkinter import CTkToplevel, CTkLabel, CTkButton

from utils.gui_utils import center_window


class AlertView(CTkToplevel):
    def __init__(self, master, title, message, **kwargs):
        super().__init__(master, **kwargs)

        self.title(title)
        self.configure(fg_color="#2E333C", bg_color="#2C2E33")

        # Centraliza a janela
        center_window(self, (400, 200))

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        self.message_label = CTkLabel(self, text=message, font=("Tahoma", 11))
        self.message_label.pack(padx=10, pady=10)

        self.confirm_button = CTkButton(self, text="OK", command=None)
        self.confirm_button.pack(padx=10, pady=10)

        self.cancel_button = CTkButton(self, text="Cancelar", command=None)
        self.cancel_button.pack(padx=10, pady=10)
