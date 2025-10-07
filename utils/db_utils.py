from models.sector_model import Sector
from models.person_model import Person
from models.task_model import Task
from models.distribution_model import Distribution
from models.assignment_model import Assignment

def gen_sample_data():

    data = {
        "sectors": [],
        "people": [],
        "tasks": [],
        "distros": [],
        "assignments": []
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
    data["tasks"].append(Task(name="Projetar um controlador", description="Projetar um controlador", sector=data["sectors"][0], priority="Alta", company="CidadeSoft", status="Concluída"))
    data["tasks"].append(Task(name="Emitir uma nota", description="uma", sector=data["sectors"][1], priority="Média", company="Petrobras"))
    data["tasks"].append(Task(name="Comprar uma lapiseira", description="Comprar uma lapiseira", sector=data["sectors"][2], priority="Baixa", company="Eletrobras"))

    data["distros"].append(Distribution(
        name="Distribuição 1",
        total_tasks=3,
        finished_tasks=1
    ))

    for sector in data["sectors"]:
        sector.save()

    for person in data["people"]:
        person.save()

    for task in data["tasks"]:
        task.save()

    for distro in data["distros"]:
        distro.save()

    data["assignments"].append(Assignment(
        distro=data["distros"][0],
        person=data["people"][0],
        task=data["tasks"][0]
    ))

    data["assignments"].append(Assignment(
        distro=data["distros"][0],
        person=data["people"][1],
        task=data["tasks"][1]
    ))

    data["assignments"].append(Assignment(
        distro=data["distros"][0],
        person=data["people"][2],
        task=data["tasks"][2]
    ))

    for assignment in data["assignments"]:
        assignment.save()

