import customtkinter as ctk


class LabeledEntryView(ctk.CTkFrame):
    def __init__(self, master, label, placeholder="", **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent", corner_radius=0)

        self.label = ctk.CTkLabel(self, text=label, font=("Tahoma", 11), anchor="e")
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder if placeholder != "" else label, font=("Tahoma", 11), fg_color="transparent")

        self.label.pack(side="left", padx=(10, 0))
        self.entry.pack(side="right", fill="x", expand=True, padx=(10, 0))

    def get(self) -> str:
        """Retorna o valor informado (ou string vazia)."""
        return self.entry.get().strip()
