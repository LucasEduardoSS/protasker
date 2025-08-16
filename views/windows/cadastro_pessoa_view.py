from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkComboBox

from utils.gui import center_window
from models.person_model import Person
from views.windows.base_window_view import BaseWindowView
from views.components.card_view import CardView
from views.components.labeled_entry_view import LabeledEntryView
from views.components.sector_entry_view import SectorField


class CadastroPessoaView(BaseWindowView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cadastro de Pessoa")
        self.minsize(300, 200)
        self._build_ui()

        # agenda para rodar após o pack/layout
        self.after(0, lambda: center_window(self, (300, 200)))

    def _build_ui(self):
        # Frame principal
        main_frame = CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=5, pady=5, fill="both", expand=True)

        # Campos de entrada
        self.entries.update({
            "name": LabeledEntryView(main_frame, "Nome"),
            "role": LabeledEntryView(main_frame, "Cargo"),
            "sector": SectorField(main_frame),
            "company": LabeledEntryView(main_frame, "Empresa")
        })

        for widget in self.entries.values():
            widget.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # Botão de salvar
        btn = CTkButton(self, text="Salvar", font=("Tahoma", 11), command=self._on_save)
        btn.pack(pady=(0, 20))

    def _on_save(self):
        data = self.get_data()
        data["sector"] = self.entries["sector"][1].get()
        CardView(self.tab_info["tab_meta"]["cards_container"], data)
        # aqui validações específicas de Pessoa, se precisar
        Person.create(**data)
        self.destroy()  # fecha a janela ou limpa campos
