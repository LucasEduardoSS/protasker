from utils.gui import center_window
from models.sector_model import Sector
from views.windows.register.register_base_view import BaseWindowView
from views.components.forms_buttons.labeled_entry_view import LabeledEntryView
from views.components.card_view import CardSetor
from views.components.list_item_view import ListItemSetor

class CadastroSetorView(BaseWindowView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cadastro de Setor")

        # agenda para rodar após o pack/layout
        self.after(0, lambda: center_window(self, (300, 100)))

        # Campos do formulário
        self.entries.update({
            "name": LabeledEntryView(self.main_frame, "Nome")
        })
        self._build(self.entries)

    def _on_save(self):
        data = self.get_data()

        # Registra no banco de dados
        sector = Sector.create(**data)

        # Cria um card para exibir os dados
        card_setor = CardSetor(self.tab_info["tab_meta"]["cards_container"], data)
        self.tab_info["tab_meta"]["cards_container"].add_card(card_setor)

        # Atualiza o layout de cards
        if self.tab_info["tab_meta"]["view_mode"] == "Cards":
            self.tab_info["tab_meta"]["cards_container"].relayout()

        # Cria um item na lista de setores
        item_setor = ListItemSetor(self.tab_info["tab_meta"]["list_container"], data)
        self.tab_info["tab_meta"]["list_container"].add_item(item_setor)

        # fecha a janela ou limpa campos
        self.destroy()
