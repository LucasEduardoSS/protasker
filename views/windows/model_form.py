import customtkinter as ctk
from peewee import ForeignKeyField

from utils.format_card_info import format_card_info, LABELS_PT
from views.components.pro_widgets import ProButton
from views.components.labeled_entry import LabeledEntryView
from views.components.labeled_combobox import LabeledComboBox


class ModelForm(ctk.CTkFrame):
    """
    Cria dinamicamente um formulário baseado em um modelo PeeWee.
    Empacota os widgets em uma coluna de entrada.
    Usa combo-boxes para os campos foreign_key.
    """

    def __init__(self, master, model_class, model_info: dict, **kwargs):

        # Inicializa a classe pai
        super().__init__(master, **kwargs)

        # Configuração
        self.configure(fg_color="transparent")

        # Modelo
        self.model_class = model_class
        self.formated_model_info = format_card_info(model_info)

        # Campos do model
        self.entries = {}

        # Itera sobre todos os campos do modelo
        for name, value in model_class._meta.fields.items():
            # pula PKs automáticos
            if value.primary_key:
                continue

            print(name, value)
            print(model_info[name])

            # Traduz o nome do campo para PT-BR
            label = LABELS_PT.get(name, None)

            # Campo ForeignKey -> usa LabeledComboBox com o model relacionado
            if isinstance(value, ForeignKeyField):
                widget = LabeledComboBox(self, label, value.rel_model)
                widget.combo.set(value.rel_model.get_or_none(value.rel_model.id == model_info[name]).name)
            else:
                # Campos de texto -> usa LabeledEntryView
                widget = LabeledEntryView(self, label, model_info[name])
                #widget.entry.insert(0, model_info[name])

            widget.pack(side="top", fill="x", padx=10, pady=10)
            self.entries[name] = widget

        # Botão de salvar
        btn = ProButton(self, text="Salvar", command=self.save)
        btn.pack(side="top", anchor="s", padx=10, pady=10, fill="x", expand=True)

    def get_data(self) -> dict:
        """Retorna um dict com os valores atuais do formulário."""
        data = {}
        for name, widget in self.entries.items():
            # LabeledComboBox não expõe get() direto; usa o combo interno
            if isinstance(widget, LabeledComboBox):
                data[name] = widget.combo.get().strip()
            else:
                data[name] = widget.get().strip()
        return data

    def save(self):
        """Cria (ou atualiza) o registro no banco."""
        data = self.get_data()
        return self.model_class.create(**data)
