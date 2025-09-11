from datetime import datetime, date
from typing import Any, Dict

try:
    # Import opcional: só usado se precisarmos resolver o nome do setor por ID
    from models.sector_model import Sector
except Exception:
    Sector = None  # Evita erro em import circular em tempo de design/tests


_LABELS_PT = {
    # Comuns
    "id": "ID",
    "name": "Nome",
    "description": "Descrição",
    "company": "Empresa",
    "weight": "Peso",
    "priority": "Prioridade",
    "dependencies": "Dependências",
    "deadline": "Prazo",
    "forecast_date": "Prazo",
    "creation_date": "Criação",
    "closure_date": "Encerramento",
    "status": "Status",
    "role": "Cargo",
    "people": "Pessoas",
    "tasks": "Tarefas",

    # Setor
    "sector": "Setor",
    "sector_id": "Setor",
    "sector_name": "Setor",

    # Variações em PT que podem chegar do formulário
    "nome": "Nome",
    "descrição": "Descrição",
    "setor": "Setor",
    "empresa": "Empresa",
    "peso": "Peso",
    "prioridade": "Prioridade",
    "dependência": "Dependências",
    "prazo": "Prazo",
}


def _format_date(value: Any) -> str:
    if isinstance(value, (datetime, date)):
        # Ajuste o formato conforme necessário
        try:
            return value.strftime("%d/%m/%Y %H:%M") if isinstance(value, datetime) else value.strftime("%d/%m/%Y")
        except Exception:
            return str(value)
    return str(value)


def _resolve_sector(fields: Dict[str, Any]) -> Any:
    """
    Retorna o melhor valor para "Setor" a partir dos campos disponíveis.
    Prioriza 'sector_name'. Se não houver, tenta buscar pelo ID em 'sector'.
    """
    if "sector_name" in fields and fields["sector_name"]:
        return fields["sector_name"]

    # Variações que podem aparecer
    sector_id = fields.get("sector") or fields.get("setor") or fields.get("sector_id")
    if sector_id in (None, "", 0):
        return None

    # Evita consulta se o import falhou
    if Sector is None:
        return str(sector_id)

    try:
        # sector_id pode vir como int, str, ou até como objeto
        sid = sector_id.id if hasattr(sector_id, "id") else sector_id
        sector_obj = Sector.get_by_id(sid)
        return getattr(sector_obj, "name", str(sid))
    except Exception:
        return str(sector_id)


def format_card_info(fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza e traduz os campos de um registro para exibição em cards.
    - Traduz rótulos para PT-BR.
    - Converte IDs (ex.: setor) para nomes quando possível.
    - Remove vazios/None e campos técnicos desnecessários (ex.: id).
    - Formata datas.
    """
    if not isinstance(fields, dict):
        return {}

    # Campos a ocultar por padrão na UI
    hidden_keys = {"id"}

    # Primeiro, preparar resolução especial de Setor
    setor_val = _resolve_sector(fields)

    output: Dict[str, Any] = {}

    for key, value in fields.items():
        # Ignorar vazios e campos técnicos
        if value in (None, "") or key in hidden_keys:
            continue

        # Mapear rótulo
        label = _LABELS_PT.get(key, None)
        if label is None:
            # Se não estiver no dicionário, usa o próprio key com capitalização simples
            label = key.replace("_", " ").capitalize()

        # Substituição específica de Setor
        if key in ("sector", "setor", "sector_id", "sector_name"):
            if setor_val not in (None, ""):
                output["Setor"] = str(setor_val)
            # Não adiciona novamente o campo com rótulos duplicados
            continue

        # Formatação de datas
        if isinstance(value, (datetime, date)):
            output[label] = _format_date(value)
            continue

        # Valor padrão em string
        output[label] = str(value)

    # Garante a inclusão do setor caso não tenha sido passado
    if "Setor" not in output and setor_val not in (None, ""):
        output["Setor"] = str(setor_val)

    return output
