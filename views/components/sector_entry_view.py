import customtkinter as ctk
from models.sector_model import Sector


class SectorField(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", corner_radius=0)
        self._build()

    def _build(self):
        # rótulo
        label = ctk.CTkLabel(self, text="Setor", font=("Tahoma", 11), width=40, anchor="e")
        label.pack(side="left", padx=(10,0))

        # Botão de adicionar setor
        self.add_sector_button = ctk.CTkButton(self, width=20, text="+", font=("Tahoma", 11), command=None)
        self.add_sector_button.pack(side="right", padx=(0, 10))

        # lista de nomes vindos do DB
        setores = [s.name for s in Sector.select(Sector.name).order_by(Sector.name)]
        self.combo = ctk.CTkComboBox(self, values=setores, font=("Tahoma", 11), fg_color="#2E333C", border_color="#AAA")
        self.combo.pack(side="right", fill="x", expand=True, padx=10)

        # Desabilita o campo setor quando não houver
        if not setores:
            self.combo.set("Nenhum setor")
            self.combo.configure(state="disabled")

    def get(self) -> Sector | None:
        """Retorna a instância de Sector selecionada (ou None)."""
        name = self.combo.get().strip()
        if not name:
            return None
        return Sector.get_or_none(Sector.name == name)
