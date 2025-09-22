import customtkinter as ctk


class Tooltip:
    """
    Classe reutilizável para adicionar tooltips a widgets no projeto.
    """

    def __init__(self, widget, text, delay=300, offset=(10, 10)):
        """
        :param widget: Widget ao qual o tooltip será associado.
        :param text: Texto a ser exibido no tooltip.
        :param delay: Delay em milissegundos para exibir o tooltip.
        :param offset: Deslocamento relativo ao cursor (x, y).
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.offset = offset

        self._tooltip = None
        self._hover_event = None
        self._leave_event = None

        self._bind_events()

    def _bind_events(self):
        """Associa os eventos de mouse ao widget."""
        self._hover_event = self.widget.bind("<Enter>", self._schedule_tooltip)
        self._leave_event = self.widget.bind("<Leave>", self._hide_tooltip)

    def _schedule_tooltip(self, event):
        """Agenda a exibição do tooltip após o delay especificado."""
        self._cancel_tooltip()  # Cancela qualquer agendamento prévio
        self._tooltip_id = self.widget.after(self.delay, lambda: self._show_tooltip(event))

    def _show_tooltip(self, event):
        """Cria e exibe o tooltip."""
        # Verifica se o tooltip já existe
        if self._tooltip:
            return

        # Cria uma nova janela do tipo Toplevel
        self._tooltip = ctk.CTkToplevel(self.widget)
        self._tooltip.wm_overrideredirect(True)  # Remove a barra de título
        self._tooltip.geometry(f"+{event.x_root + self.offset[0]}+{event.y_root + self.offset[1]}")  # Posiciona o tooltip

        # Adiciona o label do tooltip
        tooltip_label = ctk.CTkLabel(
            self._tooltip,
            text=self.text,
            font=("Tahoma", 10),
            justify="left",
            anchor="w"
        )
        tooltip_label.pack(padx=10, pady=5)

    def _hide_tooltip(self, event):
        """Esconde e destrói o tooltip."""
        self._cancel_tooltip()  # Cancela a criação agendada, se existir
        if self._tooltip:
            self._tooltip.destroy()
            self._tooltip = None

    def _cancel_tooltip(self):
        """Cancela o evento de exibição agendado."""
        if hasattr(self, "_tooltip_id") and self._tooltip_id is not None:
            try:
                self.widget.after_cancel(self._tooltip_id)
            except ValueError:
                pass
            finally:
                self._tooltip_id = None

    def destroy(self):
        """Remove o tooltip e desassocia os eventos."""
        self._hide_tooltip(None)
        if self._hover_event:
            self.widget.unbind("<Enter>", self._hover_event)
        if self._leave_event:
            self.widget.unbind("<Leave>", self._leave_event)