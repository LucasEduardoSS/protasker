import customtkinter as ctk
from peewee import ForeignKeyField
from datetime import datetime

from services.data_facade import DataFacade
from utils.widgets_utils import LABELS_PT
from views.components.pro_widgets import ProButton
from views.components.pro_labeled_widgets import LabeledEntryView, LabeledComboBox


class ModelForm(ctk.CTkFrame):
    """
    Cria dinamicamente um formulário baseado em um modelo PeeWee.
    Empacota os widgets em uma coluna de entrada.
    Usa combo-boxes para os campos foreign_key.
    """

    jump_fields = ['creation_date', 'closure_date', 'status']

    def __init__(self, master, model_class, model_info: dict | None = None, **kwargs):

        # Inicializa a classe pai
        super().__init__(master, **kwargs)

        # Configuração
        self.configure(fg_color="transparent")

        # Campos do model
        self.entries = {}
        self.fk_map = {}

        # Itera sobre todos os campos do modelo
        for name, value in DataFacade.get_fields(model_class):
            # pula PKs automáticos
            if value.primary_key:
                continue

            # Traduz o nome do campo para PT-BR
            label = LABELS_PT.get(name, None)

            # Indica campo obrigatório
            if not value.null:
                label += " *"

            if isinstance(value, ForeignKeyField):
                # Guarda o modelo relacionado
                self.fk_map[name] = value.rel_model

                # Campo ForeignKey -> usa LabeledComboBox com o model relacionado
                widget = LabeledComboBox(self, label, value.rel_model)

                if model_info:  # Carrega o valor atual em caso de edição
                  widget.combo.set(DataFacade.get_record(name, model_info[name]).name if model_info[name] is not None else label)
            else:
                # Campos de texto -> usa LabeledEntryView
                widget = LabeledEntryView(self, label)

                if model_info:  # Carrega o valor atual em caso de edição
                  widget.entry.insert(0, model_info[name] if model_info[name] is not None else label)

            # pula campos ignorados
            if name not in self.jump_fields or model_info:
                widget.pack(side="top", fill="x", padx=10, pady=10)

            self.entries[name] = widget

        self.obs_label = ctk.CTkLabel(self, text="* : Campo obrigatório", font=("Tahoma", 11), anchor="w")
        self.obs_label.pack(side="top", anchor="s", padx=10, pady=0, fill="x", expand=True)

        # Botão de salvar
        self.save_btn = ProButton(self, text="Salvar", command=None)
        self.save_btn.pack(side="top", anchor="s", padx=10, pady=10, fill="x", expand=True)

    def get_data(self) -> dict:
        """ Retorna um dict com os valores atuais do formulário. """
        data = {}

        for name, widget in self.entries.items():
            if name == "creation_date":
                data[name] = datetime.now()
                continue

            # LabeledComboBox não expõe get() direto; usa o combo interno
            if isinstance(widget, LabeledComboBox):
                selected_name = widget.get()
                model_class = self.fk_map[name]
                data[name] = model_class.get_or_none(model_class.name == selected_name)
            else:
                data[name] = widget.get()

        return data
