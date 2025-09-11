from views.components.list_item import ListItem

class ListItemPessoa(ListItem):
    def __init__(self, master, person_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self._person_meta = {
            "Nome": person_info["name"],
            "Cargo": person_info["role"],
            "Setor": person_info["sector"], # Sector.get_by_id(person_info["sector"]).name if person_info["sector"] is not None else None,
            "Empresa": person_info["company"]
        }
        self.load_fields(self._person_meta)


class ListItemTarefa(ListItem):
    def __init__(self, master, task_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da tarefa
        self._task_meta = {
            "Tarefa": task_info["name"],
            "Descrição": task_info["description"],
            "Setor": task_info["sector"], # Sector.get_by_id(task_info["sector"]).name if task_info["sector"] is not None else None,
            "Prioridade": task_info["priority"],
            "Status": "Pendente",
            "Prazo": task_info["deadline"]
        }
        self.load_fields(self._task_meta)


class ListItemSetor(ListItem):
    def __init__(self, master, sector_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self._sector_meta = {
            "Setor": sector_info["name"]
        }
        self.load_fields(self._sector_meta)


class ListItemDistribuicao(ListItem):
    def __init__(self, master, distr_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self._distr_meta = {
            "Pessoas": distr_info["people"],
            "Tarefas": distr_info["tasks"]
        }
        self.load_fields(self._distr_meta)
