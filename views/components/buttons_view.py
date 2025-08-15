import customtkinter as ctk
from typing import Callable, List

class VerticalSegmented(ctk.CTkFrame):
    """
    Simula um CTkSegmentedButton vertical, empilhando CTkButtons.
    values: lista de rótulos
    command: callback(value) ao clicar
    """
    def __init__(
        self,
        master,
        values: List[str],
        command: Callable[[str], None] = None,
        *,
        width: int = 100,
        corner_radius: int = 0,
        fg_color: str = "#2C2E33",
        selected_color: str = "#5A5E68",
        unselected_color: str = "#393E4A",
        font: tuple = ("Tahoma", 11),
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self._command = command
        self._buttons = {}
        self._sel_color = selected_color
        self._unsel_color = unselected_color

        for v in values:
            btn = ctk.CTkButton(
                self,
                text=v,
                width=width,
                corner_radius=corner_radius,
                fg_color=unselected_color,
                hover_color=unselected_color,
                font=font,
                command=lambda vv=v: self._on_click(vv)
            )
            btn.pack(side="top", fill="x", expand=True)
            self._buttons[v] = btn

        # opcional: selecione o primeiro por padrão
        if values:
            self.set(values[0])

    def _on_click(self, value: str):
        self.set(value)
        if self._command:
            self._command(value)

    def set(self, value: str):
        """Marca ‘value’ como selecionado e atualiza cores."""
        if value not in self._buttons:
            raise ValueError(f"value '{value}' não está em {list(self._buttons)}")
        for v, btn in self._buttons.items():
            btn.configure(fg_color=(self._sel_color if v == value else self._unsel_color))
        # opcional: ajustar hover_color também
        self._buttons[value].configure(hover_color=self._sel_color)
        self._selected = value

    def get(self) -> str:
        return getattr(self, "_selected", None)
