from utils.gui import center_window
from models.task_model import Task
from views.windows.register.register_base_view import RegisterBaseWindowView
from views.components.card import CardTarefa
from views.components.forms_buttons.labeled_entry import LabeledEntryView
from views.components.forms_buttons.labeled_combobox import SectorComboBox
from views.components.list_item import ListItemTarefa


class RegisterTaskView(RegisterBaseWindowView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cadastro de Tarefa")
        self.minsize(400, 330)

        # agenda para rodar após o pack/layout
        self.after(0, lambda: center_window(self, (400, 330)))

        # Campos de entrada
        self.entries.update({
            "name": LabeledEntryView(self.main_frame, "Nome"),
            "description": LabeledEntryView(self.main_frame, "Descrição"),
            "sector": SectorComboBox(self.main_frame, "Setor"),
            "company": LabeledEntryView(self.main_frame, "Empresa"),
            "priority": LabeledEntryView(self.main_frame, "Prioridade", "Baixa, Média, Alta"),
            "dependencies": LabeledEntryView(self.main_frame, "Dependências"),
            "deadline": LabeledEntryView(self.main_frame, "Data limite", "dd/mm/aaaa")
        })
        self._build(self.entries)

    def _on_save(self):
        data = self.get_data()

        # Cria um card para exibir os dados
        card_tarefa = CardTarefa(self.tab_info["tab_meta"]["cards_container"], data)
        self.tab_info["tab_meta"]["cards_container"].add_card(card_tarefa)

        if self.tab_info["tab_meta"]["view_mode"] == "Cards":
          self.tab_info["tab_meta"]["cards_container"].relayout()

        # Cria um item na lista de tarefas
        item_tarefa = ListItemTarefa(self.tab_info["tab_meta"]["list_container"], data)
        self.tab_info["tab_meta"]["list_container"].add_item(item_tarefa)

        # Registra no banco de dados
        Task.create(**data)

        # fecha a janela ou limpa campos
        self.destroy()
