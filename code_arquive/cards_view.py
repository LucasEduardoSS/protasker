class CardPessoa():
    def __init__(self, master, person_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da pessoa
        self._card_meta = {
            "Nome": person_info["name"],
            "Cargo": person_info["role"],
            #"Setor": Sector.get_by_id(person_info["sector"]).name if person_info["sector"] is not None else None,
            "Empresa": person_info["company"]
        }
        self.load_fields(self._card_meta)


class CardTarefa():
    def __init__(self, master, task_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da tarefa
        self._card_meta = {
            "Tarefa": task_info["name"],
            "Descrição": task_info["description"],
            #"Setor": Sector.get_by_id(task_info["sector"]).name if task_info["sector"] is not None else None,
            "Empresa": task_info["company"],
            "Prioridade": task_info["priority"],
            "Prazo": task_info["deadline"],
            "Status": "Pendente"
        }
        self.load_fields(self._card_meta)


class CardSetor():
    def __init__(self, master, sector_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos do setor
        self._card_meta = {
            "Setor": sector_info["name"]
        }
        self.load_fields(self._card_meta)