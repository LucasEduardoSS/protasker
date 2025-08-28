from models.sector_model import Sector
from models.person_model import Person
from models.task_model import Task

def gen_sample_data():

    data = {
        "sectors": [],
        "people": [],
        "tasks": []
    }

    # Setores
    data["sectors"].append(Sector(name="Engenharia"))
    data["sectors"].append(Sector(name="Financeiro"))
    data["sectors"].append(Sector(name="Compras"))

    # Pessoas
    data["people"].append(Person(name="Lucas Eduardo", role="Engenheiro", sector=data["sectors"][0], company="CidadeSoft"))
    data["people"].append(Person(name="Robinho", role="Contador", sector=data["sectors"][1], company="Petrobras"))
    data["people"].append(Person(name="Valdemar", role="Comprador", sector=data["sectors"][2], company="Eletrobras"))

    # Tarefas
    data["tasks"].append(Task(name="Projetar um controlador", description="Projetar um controlador", sector=data["sectors"][0], priority="Alta", dependencies="", company="CidadeSoft"))
    data["tasks"].append(Task(name="Emitir uma nota", description="uma", sector=data["sectors"][1], priority="Média", dependencies="", company="Petrobras"))
    data["tasks"].append(Task(name="Comprar uma lapiseira", description="Comprar uma lapiseira", sector=data["sectors"][2], priority="Baixa", dependencies="", company="Eletrobras"))

    for sector in data["sectors"]:
        sector.save()

    for person in data["people"]:
        person.save()

    for task in data["tasks"]:
        task.save()
