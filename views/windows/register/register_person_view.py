from utils.gui import center_window
from models.person_model import Person
from views.windows.register.register_base_view import BaseWindowView
from views.components.card_view import CardPessoa
from views.components.forms_buttons.labeled_entry_view import LabeledEntryView
from views.components.forms_buttons.labeled_combobox_view import SectorField
from views.components.list_item_view import ListItemPessoa


class CadastroPessoaView(BaseWindowView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cadastro de Pessoa")
        self.minsize(300, 220)

        # agenda para rodar após o pack/layout
        self.after(0, lambda: center_window(self, (300, 220)))

        # Campos de entrada
        self.entries.update({
            "name": LabeledEntryView(self.main_frame, "Nome"),
            "role": LabeledEntryView(self.main_frame, "Cargo"),
            "sector": SectorField(self.main_frame, "Setor"),
            "company": LabeledEntryView(self.main_frame, "Empresa")
        })
        self._build(self.entries)

    def _on_save(self):
        data = self.get_data()

        # Cria um card para exibir os dados
        card_pessoa = CardPessoa(self.tab_info["tab_meta"]["cards_container"], data)
        self.tab_info["tab_meta"]["cards_container"].add_card(card_pessoa)

        if self.tab_info["tab_meta"]["view_mode"] == "Cards":
          self.tab_info["tab_meta"]["cards_container"].relayout()

        # Cria um item na lista de pessoas
        item_pessoa = ListItemPessoa(self.tab_info["tab_meta"]["list_container"], data)
        self.tab_info["tab_meta"]["list_container"].add_item(item_pessoa)

        # Registra no banco de dados
        Person.create(**data)

        # fecha a janela ou limpa campos
        self.destroy()
