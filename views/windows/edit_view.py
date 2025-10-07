from customtkinter import CTkToplevel

from views.windows.model_form import ModelForm
from utils.gui_utils import center_window
from services.data_facade import DataFacade
from database.db import get_database


class EditView(CTkToplevel):
    def __init__(self,
                 title: str,
                 model_cls,
                 model_info: dict | None = None,
                 tab_name = None,
                 on_save = None,
                 **kwargs):

        # Inicializa a classe pai
        super().__init__(**kwargs)

        # Atributos
        self.entries = {}
        self.tab_name = tab_name
        self.model_cls = model_cls
        self.model_info = model_info
        self.on_save = on_save

        # Configuração da janela
        self.title(title)
        self.configure(fg_color="#2E333C")
        self.minsize(300,100)
        self.iconbitmap("images/protasker_icon.ico")

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Frame principal
        self.main_frame = ModelForm(self, model_cls, model_info)
        self.main_frame.pack(padx=5, pady=5, fill="both", expand=True)
        self.main_frame.save_btn.configure(command=self._on_save)

        # Atualiza o tamanho e centraliza antes de exibir
        self.update()
        center_window(self, (self._current_width, self._current_height))

    def _on_save(self):
        """Atualiza os dados no banco de dados e fecha a janela."""

        # Dados do formulário
        data = self.main_frame.get_data()

        # Registro atual
        if self.model_info:
          record_id = self.model_info.get("id")
        else:
          record_id = None

        # Atualiza ou cria no banco de dados
        db = get_database()
        with db.atomic():
            if record_id:
                DataFacade.update_record(self.model_cls, record_id, data)
                # Adiciona o ID ao dicionário para o callback
                data['id'] = record_id
            else:
                # create_record retorna a nova instância do modelo
                new_record = DataFacade.create_record(self.model_cls, data)
                # Adiciona o ID do novo registro ao dicionário
                data['id'] = new_record.id

        # Chama a função de callback
        if callable(self.on_save):
            if self.tab_name:
                self.on_save(self.tab_name, data)
            else:
                self.on_save(data)

        # fecha a janela ou limpa campos
        self.destroy()
