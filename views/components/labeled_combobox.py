import customtkinter as ctk


class LabeledComboBox(ctk.CTkFrame):
    def __init__(self, master, label, model, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", corner_radius=0)

        # Valores do combobox
        model_values: list = [model.name for model in model.select()]

        # Rótulo
        label = ctk.CTkLabel(self, text=label, font=("Tahoma", 11), anchor="e")
        label.pack(side="left", padx=(10,0))

        # Botão de adicionar um registro
        self.add_sector_button = ctk.CTkButton(self, width=25, text="+", font=("Tahoma", 11), command=None)
        self.add_sector_button.pack(side="right")

        # ComboBox
        self.combo = ctk.CTkComboBox(self, values=model_values, font=("Tahoma", 11), fg_color="#2E333C", border_color="#AAA")
        self.combo.pack(side="right", fill="x", padx=(10, 5), expand=True)

        # Desabilita o campo quando não houver valores registrados
        if not model_values:
            self.combo.set(f"Nenhum {label.lower()}")
            self.combo.configure(state="disabled")
