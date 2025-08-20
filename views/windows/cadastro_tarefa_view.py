from utils.gui import center_window
from models.task_model import Task
from views.windows.base_window_view import BaseWindowView
from views.components.card_view import CardTarefa
from views.components.labeled_entry_view import LabeledEntryView
from views.components.labeled_combobox_view import SectorField
from views.components.list_item_view import ListItemTarefa


class CadastroTarefaView(BaseWindowView):
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
            "sector": SectorField(self.main_frame, "Setor"),
            "priority": LabeledEntryView(self.main_frame, "Prioridade", "Baixa, Média, Alta"),
            "dependencies": LabeledEntryView(self.main_frame, "Dependências"),
            "urgent": LabeledEntryView(self.main_frame, "Urgente", "Sim / Não"),
            "forecast_date": LabeledEntryView(self.main_frame, "Data prevista", "dd/mm/aaaa"),
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
