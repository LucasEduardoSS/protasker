'''class SectorComboBox(LabeledComboBox):
    def __init__(self, master, label, **kwargs):
        super().__init__(master, **kwargs)
        self._build(label, [s.name for s in Sector.select(Sector.name).order_by(Sector.name)])

    def get(self) -> Sector | None:
        """Retorna a instância de Sector selecionada (ou None)."""
        name = self.combo.get().strip()
        if not name:
            return None
        return Sector.get_or_none(Sector.name == name)'''


'''class TaskComboBox(LabeledComboBox):
    def __init__(self, master, label: str, **kwargs):
        super().__init__(master, **kwargs)
        self._build(label, [t.name for t in Task.select(Task.name).order_by(Task.name)])

    def get(self) -> Task | None:
        """Retorna a instância de Task selecionada (ou None)."""
        name = self.combo.get().strip()
        if not name:
            return None
        return Task.get_or_none(Task.name == name)'''
