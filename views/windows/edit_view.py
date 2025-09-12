from customtkinter import CTkToplevel

from views.windows.model_form import ModelForm


class EditBaseWindowView(CTkToplevel):
    def __init__(self, model, model_info: dict, **kwargs):

        # Inicializa a classe pai
        super().__init__(**kwargs)

        # Atributos
        self.entries = {}
        self.data = None

        # Configuração da janela
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Frame principal
        self.main_frame = ModelForm(self, model, model_info)
        self.main_frame.pack(padx=5, pady=5, fill="both", expand=True)

    def _on_save(self):
        """Atualiza os dados no banco de dados e fecha a janela."""
        self.data = self.main_frame.get_data()

        # Recarrega os registros

        # Registra no banco de dados (somente se houver model válido)
        if self.model is not None:
            self.model.create(**self.data)
        else:
            # Caso o model não tenha sido injetado, evita crash e informa no console
            print("Aviso: nenhum 'model' foi fornecido em tab_info; dados não foram persistidos.")

        # fecha a janela ou limpa campos
        self.destroy()
