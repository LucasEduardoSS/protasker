from customtkinter import CTkFrame, CTkButton

from models.person_model import Person
from views.windows.base_window_view import BaseWindowView
from views.components.labeled_entry_view import LabeledEntryView

class CadastroSetorView(BaseWindowView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cadastro de Setor")
        self._build_ui()

    def _build_ui(self):
        # Frame principal
        main_frame = CTkFrame(self, width=400, height=300)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Campos de entrada
        name = LabeledEntryView(main_frame, "Nome")
        role = LabeledEntryView(main_frame, "Cargo")
        sector = LabeledEntryView(main_frame, "Setor")
        company = LabeledEntryView(main_frame, "Empresa")

        self.entries = {
            "name": LabeledEntryView(main_frame, "Nome"),
            "role": LabeledEntryView(main_frame, "Cargo"),
            "sector": LabeledEntryView(main_frame, "Setor"),
            "company": LabeledEntryView(main_frame, "Empresa")
        }

        # Botão de salvar
        btn = CTkButton(self, text="Salvar", font=("Tahoma", 11), command=self._on_save)
        btn.pack(pady=(0, 20))

    def _on_save(self):
        data = self.get_data()
        # aqui validações específicas de Pessoa, se precisar
        Person.create(**data)
        self.destroy()  # fecha a janela ou limpa campos
