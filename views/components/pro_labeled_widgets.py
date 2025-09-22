import customtkinter as ctk


class LabeledComboBox(ctk.CTkFrame):
    def __init__(self, master, label, model, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", corner_radius=0)

        # Valores do combobox
        model_values: list = [model.name for model in model.select()]

        # Rótulo
        self.label = ctk.CTkLabel(self, text=label, font=("Tahoma", 11), anchor="e")
        self.label.pack(side="left", padx=(10,0))

        # ComboBox
        self.combo = ctk.CTkComboBox(self, values=model_values, font=("Tahoma", 11), fg_color="#2E333C", border_color="#AAA")
        self.combo.pack(side="right", fill="x", padx=(10, 0), expand=True)

        # Desabilita o campo quando não houver valores registrados
        if not model_values:
            self.combo.set(f"Nenhum {label.lower()}")
            self.combo.configure(state="disabled")

    def get(self) -> str:
        """Retorna o valor selecionado (ou string vazia)."""
        return self.combo.get().strip()


class LabeledEntryView(ctk.CTkFrame):
    def __init__(self, master, label, placeholder="", **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent", corner_radius=0)

        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=("Tahoma", 11),
            anchor="e"
        )

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder if placeholder != "" else label,
            font=("Tahoma", 11),
            fg_color="transparent",
            border_color="#777"
        )

        self.label.pack(side="left", padx=(10, 0))
        self.entry.pack(side="right", fill="x", expand=True, padx=(10, 0))

    def get(self) -> str:
        """Retorna o valor informado (ou string vazia)."""
        return self.entry.get().strip()
