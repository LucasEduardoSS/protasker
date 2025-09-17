from datetime import datetime, date
from typing import Any, Dict

from models.sector_model import Sector


LABELS_PT = {
    # Comuns
    "id": "ID",
    "name": "Nome",
    "description": "Descrição",
    "company": "Empresa",
    "sector": "Setor",
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
    "tasks": "Tarefas"
}


def _format_date(value: Any) -> str:
    if isinstance(value, (datetime, date)):
        # Ajuste o formato conforme necessário
        try:
            return value.strftime("%d/%m/%Y %H:%M") if isinstance(value, datetime) else value.strftime("%d/%m/%Y")
        except Exception:
            return str(value)
    return str(value)


def format_card_info(fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza e traduz os campos de um registro para exibição em cards.
    - Traduz rótulos para PT-BR.
    - Remove vazios/None e campos técnicos desnecessários (ex.: id).
    - Formata datas.
    """
    if not isinstance(fields, dict):
        return {}

    # Campos a ocultar por padrão na UI
    hidden_keys = {"id"}

    output: Dict[str, Any] = {}

    for key, value in fields.items():
        # Ignorar vazios e campos técnicos
        if value in (None, "") or key in hidden_keys:
            continue

        # Mostra o nome do setor
        if key == "sector":
            value = Sector.get_by_id(value)

        # Mapear rótulo
        label = LABELS_PT.get(key, None)
        if label is None:
            # Se não estiver no dicionário, usa o próprio key com capitalização simples
            label = key.replace("_", " ").capitalize()

        # Formatação de datas
        if isinstance(value, (datetime, date)):
            output[label] = _format_date(value)
            continue

        # Valor padrão em string
        output[label] = str(value)

    return output


def propagate_hover_bind(p_widget, hover_fg: str, normal_fg: str = None):
    """
    Propaga hover para widgets filhos.
    Por padrão, a cor dos widgets filhos volta para transparent.
    """

    def _on_hover_enter(widget):
        """Troca a cor do frame ao passar o mouse."""
        widget.configure(fg_color=hover_fg)

    def _on_hover_leave(widget):
        """Restaura a cor normal do frame quando o mouse sai."""
        widget.configure(fg_color=normal_fg if normal_fg else "transparent")

    # Hover leve (evita mudança contínua em <Motion>)
    p_widget.bind("<Enter>", lambda e: _on_hover_enter(p_widget), add="+")
    p_widget.bind("<Leave>", lambda e: _on_hover_leave(p_widget), add="+")

    for child in p_widget.winfo_children():
        child.bind("<Enter>", lambda e: _on_hover_enter(p_widget), add="+")
        child.bind("<Leave>", lambda e: _on_hover_leave(p_widget), add="+")

        if hasattr(child, "winfo_children"):
            for subchild in child.winfo_children():
                subchild.bind("<Enter>", lambda e: _on_hover_enter(p_widget), add="+")
                subchild.bind("<Leave>", lambda e: _on_hover_leave(p_widget), add="+")
