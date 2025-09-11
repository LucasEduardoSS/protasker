import customtkinter as ctk

class ModelForm(ctk.CTkFrame):
    """
    Cria dinamicamente um formulário baseado em um modelo PeeWee.
    """
    def __init__(self, master, model_class, widget_overrides: dict[str, ctk.CTkBaseClass] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.model_class = model_class
        self.entries = {}
        self._overrides = widget_overrides or {}

        # Itera sobre todos os campos do modelo
        row = 0
        for name, field in self.model_class._meta.fields.items():
            # pula PKs automáticos
            if field.primary_key:
                continue

            if field.foreign_key:
                continue

            # Label
            lbl = ctk.CTkLabel(self, text=name.replace("_", " ").title(), font=("Tahoma", 11))
            lbl.grid(row=row, column=0, sticky="e", padx=5, pady=5)

            # Widget: override ou entry padrão
            if name in self._overrides:
                widget = self._overrides[name](self)
            else:
                widget = ctk.CTkEntry(
                    self, placeholder_text=f"Digite {name}", font=("Tahoma", 11)
                )

            widget.grid(row=row, column=1, sticky="we", padx=5, pady=5)
            self.entries[name] = widget
            row += 1

        # Faz coluna 1 (entries) expandir
        self.grid_columnconfigure(1, weight=1)

    def get_data(self) -> dict:
        """Retorna um dict com os valores atuais do formulário."""
        data = {}
        for name, widget in self.entries.items():
            data[name] = widget.get().strip()
        return data

    def save(self):
        """Cria (ou atualiza) o registro no banco."""
        data = self.get_data()
        return self.model_class.create(**data)
