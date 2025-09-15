import customtkinter as ctk
from peewee import ForeignKeyField

from utils.format_card_info import LABELS_PT
from views.components.pro_widgets import ProButton
from views.components.labeled_entry import LabeledEntryView
from views.components.labeled_combobox import LabeledComboBox


class ModelForm(ctk.CTkFrame):
    """
    Cria dinamicamente um formulário baseado em um modelo PeeWee.
    Empacota os widgets em uma coluna de entrada.
    Usa combo-boxes para os campos foreign_key.
    """

    def __init__(self, master, model_class, model_info: dict | None = None, **kwargs):

        # Inicializa a classe pai
        super().__init__(master, **kwargs)

        # Configuração
        self.configure(fg_color="transparent")

        # Campos do model
        self.entries = {}
        self.fk_map = {}

        # Itera sobre todos os campos do modelo
        for name, value in model_class.get_meta().fields.items():
            # pula PKs automáticos
            if value.primary_key:
                continue

            # Traduz o nome do campo para PT-BR
            label = LABELS_PT.get(name, None)

            if isinstance(value, ForeignKeyField):
                # Guarda o modelo relacionado
                self.fk_map[name] = value.rel_model

                # Campo ForeignKey -> usa LabeledComboBox com o model relacionado
                widget = LabeledComboBox(self, label, value.rel_model)

                if model_info:  # Carrega o valor atual em caso de edição
                  widget.combo.set(value.rel_model.get_or_none(value.rel_model.id == model_info[name]).name)
            else:
                # Campos de texto -> usa LabeledEntryView
                widget = LabeledEntryView(self, label)

                if model_info:  # Carrega o valor atual em caso de edição
                  widget.entry.insert(0, model_info[name] if model_info[name] is not None else label)

            widget.pack(side="top", fill="x", padx=10, pady=10)
            self.entries[name] = widget

        # Botão de salvar
        self.save_btn = ProButton(self, text="Salvar", command=None)
        self.save_btn.pack(side="top", anchor="s", padx=10, pady=10, fill="x", expand=True)

    def get_data(self) -> dict:
        """Retorna um dict com os valores atuais do formulário."""
        data = {}
        for name, widget in self.entries.items():
            # LabeledComboBox não expõe get() direto; usa o combo interno
            if isinstance(widget, LabeledComboBox):
                data[name] = self.fk_map[name].get_by_name(widget.get())
            else:
                data[name] = widget.get().strip()
        return data
