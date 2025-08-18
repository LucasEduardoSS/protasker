from customtkinter import CTkFrame, CTkButton

from utils.gui import center_window
from models.person_model import Person
from views.windows.base_window_view import BaseWindowView
from views.components.card_view import CardPessoa
from views.components.labeled_entry_view import LabeledEntryView
from views.components.sector_entry_view import SectorField


class CadastroPessoaView(BaseWindowView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cadastro de Pessoa")
        self.minsize(300, 220)
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

        # Posiciona os campos
        for widget in self.entries.values():
            widget.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # Botão de salvar
        btn = CTkButton(self, height=30, text="Salvar", font=("Tahoma", 11), command=self._on_save)
        btn.pack(side="top", anchor="s", padx=10, pady=10, fill="x", expand=True)

    def _on_save(self):
        data = self.get_data()

        # Cria um card para exibir os dados
        card_pessoa = CardPessoa(self.tab_info["tab_meta"]["cards_container"], data)
        self.tab_info["tab_meta"]["cards_container"].add_card(card_pessoa)

        if self.tab_info["tab_meta"]["view_mode"] == "Cards":
          self.tab_info["tab_meta"]["cards_container"].relayout()

        # Cria um item na lista de pessoas
        #item_pessoa = ItemList

        # Registra no banco de dados
        Person.create(**data)

        # fecha a janela ou limpa campos
        self.destroy()
