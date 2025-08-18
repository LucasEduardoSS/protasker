import customtkinter as ctk


class BaseWindowView(ctk.CTkToplevel):
    def __init__(self, tab_info: dict, **kwargs):
        super().__init__(**kwargs)

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Configurações
        self.configure(fg_color="#2E333C")

        self.tab_info = tab_info
        self.entries = {}

    def get_data(self) -> dict:
        """Retorna um dict com os valores atuais do formulário."""
        data = {}
        for name, widget in self.entries.items():
            data[name] = widget.get()
        return data
