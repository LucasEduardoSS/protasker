from dataclasses import dataclass, field
from typing import List, Tuple
from contextlib import contextmanager
from random import shuffle
from peewee import IntegrityError

# Modelos Peewee
# Importados apenas para typing
from models.person_model import Person
from models.task_model import Task
from models.assignment_model import Assignment
from models.distribution_model import Distribution

# Services
from services.assignment_service import AssignmentService


@dataclass(order=True)
class _Bucket:
    load: int
    index: int
    person: Person = field(compare=False)
    tasks: List[Task] = field(default_factory=list, compare=False)


@contextmanager
def _atomic_if(database_obj):
    if database_obj is None:
        yield
    else:
        with database_obj.atomic():
            yield

def _resolve_db():
    """Retorna a instância de Database associada aos modelos (Peewee)."""
    return getattr(getattr(Assignment, "_meta", None), "database", None)


def allocate_tasks(
        distro: Distribution,
        people: List[Person],
        tasks: List[Task],
        *,
        clear_existing_for_people: bool = False,
    ) -> List[Tuple[Person, List[Task]]] | None:
    """
    Distribui tarefas de forma justa entre pessoas usando Best-Fit Decreasing.

    - Usa Task.weight (int) como métrica de carga.
    - Considera o setor das tarefas e das pessoas (tarefas só são atribuídas a pessoas do mesmo setor).
    - Retorna uma lista de (pessoa, [tarefas]) para uso imediato.
    - Se 'assignment_model' for fornecido (um modelo de junção do Peewee como Assignment),
      a função também persistirá os vínculos pessoa ↔ tarefa em uma única transação.

    Parâmetros:
        people: Iterável de Person (já filtrado).
        tasks:  Iterável de Task (já filtrado).
        clear_existing_for_people: Se True e persistindo, exclui linhas existentes
                                   em assignment_model para essas pessoas antes de inserir.

    Retorna:
        List[Tuple[Person, List[Task]]], preservando a ordem de entrada das pessoas.
    """

    # Embaralha a lista de pessoas
    shuffle(people)

    if not people:
        return []

    # Prepara baldes (estável pela ordem de entrada)
    buckets = [_Bucket(load=0, index=i, person=p) for i, p in enumerate(people)]

    # Mais pesadas primeiro para melhorar o balanceamento
    tasks_desc = sorted(tasks, key=lambda e: int(getattr(e, "weight", 0) or 0), reverse=True)

    # Alocação gulosa: menor carga → menos tarefas → índice estável
    # Agora considerando o setor da tarefa e da pessoa
    for task in tasks_desc:
        weight = int(getattr(task, "weight", 0) or 0)
        task_sector = getattr(task, "sector", None)
        
        # Filtra buckets (pessoas) do mesmo setor da tarefa
        eligible_buckets = [
            b for b in buckets 
            if getattr(b.person, "sector", None) == task_sector
        ]
        
        # Se não houver pessoas elegíveis do mesmo setor, pula a tarefa
        if not eligible_buckets:
            return None
        
        # Seleciona o bucket com menor carga entre os elegíveis
        bucket = min(eligible_buckets, key=lambda x: (x.load, len(x.tasks), x.index))
        bucket.tasks.append(task)
        bucket.load += weight

    plan: List[Tuple[Person, List[Task]]] = [(bucket.person, bucket.tasks) for bucket in buckets]

    # Persistência
    db = _resolve_db()
    with _atomic_if(db):

        # Limpa as atribuições existentes para essas pessoas
        if clear_existing_for_people:
            AssignmentService.delete_assignments(person_ids=[p.id for p, _ in plan])

        try:
            # Use get_or_create para evitar duplicatas se unique(person, task) estiver aplicado
            for person, ts in plan:
                for task in ts:
                    Assignment.get_or_create(distro=distro, person=person, task=task)
        except Exception:
            db.rollback()
            raise IntegrityError(f"Tarefa '{task}' já distribuida.")

    return plan
