import customtkinter as ctk


class ModelForm(ctk.CTkFrame):
    """
    Cria dinamicamente um formulário baseado em um modelo PeeWee.
    """
    def __init__(self, master, model_class, **kwargs):
        super().__init__(master, **kwargs)
        self.model_class = model_class
        self.entries = {}

        # Itera sobre todos os campos do modelo
        row = 0
        for name, field in self.model_class._meta.fields.items():
            # pula PKs automáticos
            if field.primary_key:
                continue

            # Label
            lbl = ctk.CTkLabel(self, text=name.replace("_", " ").title(), font=("Tahoma", 11))
            lbl.grid(row=row, column=0, sticky="e", padx=5, pady=5)

            # Entry (aqui você pode criar tipos diferentes conforme field)
            ent = ctk.CTkEntry(self, placeholder_text=f"Digite {name}", font=("Tahoma", 11))
            ent.grid(row=row, column=1, sticky="we", padx=5, pady=5)

            self.entries[name] = ent
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
