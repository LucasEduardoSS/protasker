from customtkinter import CTkFrame, CTkButton, CTkToplevel


class RegisterBaseWindowView(CTkToplevel):
    def __init__(self, tab_info: dict, **kwargs):
        super().__init__(**kwargs)
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Frame principal
        self.main_frame = CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(padx=5, pady=5, fill="both", expand=True)

        self.tab_info = tab_info
        self.entries = {}
        self.data = None

    def _build(self, entries: dict):
        # Posiciona os campos
        for widget in entries.values():
            widget.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # Botão de salvar
        btn = CTkButton(self, height=30, text="Salvar", font=("Tahoma", 11), command=self._on_save)
        btn.pack(side="top", anchor="s", padx=10, pady=10, fill="x", expand=True)

    def get_data(self) -> dict:
        """Retorna um dict com os valores atuais do formulário."""
        data = {}
        for name, widget in self.entries.items():
           data[name] = widget.get()
        return data

    def _on_save(self):
        self.data = self.get_data()
