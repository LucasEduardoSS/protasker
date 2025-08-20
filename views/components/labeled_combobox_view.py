import customtkinter as ctk

from models.sector_model import Sector
from models.task_model import Task

class LabeledComboBox(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", corner_radius=0)

    def _build(self, p_label, p_values):
        # Rótulo
        label = ctk.CTkLabel(self, text=p_label, font=("Tahoma", 11), anchor="e")
        label.pack(side="left", padx=(10,0))

        # Botão de adicionar um registro
        self.add_sector_button = ctk.CTkButton(self, width=25, text="+", font=("Tahoma", 11), command=None)
        self.add_sector_button.pack(side="right")

        # ComboBox
        self.combo = ctk.CTkComboBox(self, values=p_values, font=("Tahoma", 11), fg_color="#2E333C", border_color="#AAA")
        self.combo.pack(side="right", fill="x", padx=(10, 5), expand=True)

        # Desabilita o campo quando não houver valores registrados
        if not p_values:
            self.combo.set(f"Nenhum {p_label.lower()}")
            self.combo.configure(state="disabled")


class SectorField(LabeledComboBox):
    def __init__(self, master, label, **kwargs):
        super().__init__(master, **kwargs)
        self._build(label, [s.name for s in Sector.select(Sector.name).order_by(Sector.name)])

    def get(self) -> Sector | None:
        """Retorna a instância de Sector selecionada (ou None)."""
        name = self.combo.get().strip()
        if not name:
            return None
        return Sector.get_or_none(Sector.name == name)


class DependenciesField(LabeledComboBox):
    def __init__(self, master, label: str, **kwargs):
        super().__init__(master, **kwargs)
        self._build(label, [t.name for t in Task.select(Task.name).order_by(Task.name)])

    def get(self) -> Task | None:
        """Retorna a instância de Task selecionada (ou None)."""
        name = self.combo.get().strip()
        if not name:
            return None
        return Task.get_or_none(Task.name == name)
