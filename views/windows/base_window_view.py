import customtkinter as ctk
from peewee import Model

from models.pessoa_model import Pessoa
from models.tarefa_model import Tarefa
from models.setor_model import Setor
from models.model_form import ModelForm

from views.components.card_view import CardView, CardPessoa
from views.components.record_view import ListItemView


class BaseWindowView(ctk.CTkToplevel):
    def __init__(self, tab_info: dict, title: str, **kwargs):
        super().__init__(**kwargs)

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Configurações
        self.configure(fg_color="#2E333C")
        self.title(title)
        self.minsize(250, 100)

        self.tab_info = tab_info

        # Chama o respectivo formulário
        match title:
            case "Cadastrar Pessoa":
                self.load_cadastro_view(Pessoa)
            case "Cadastrar Tarefa":
                self.load_cadastro_view(Tarefa)
            case "Cadastrar Setor":
                self.load_cadastro_view(Setor)

    def load_cadastro_view(self, model):
        # Monta o form baseado em Pessoa
        form = ModelForm(self, model, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=20)

        # Botão de salvar
        btn_salvar = ctk.CTkButton(self, font=("Tahoma", 11), text="Salvar",command=lambda: self._on_save(form))
        btn_salvar.pack(pady=(0, 20))

    def _on_save(self, form: ModelForm):
        try:
            form.save()

            match self.tab_info["tab_name"]:
                case "Pessoas":
                    self.tab_info["tab_meta"]["cards_container"].add_card(
                        CardPessoa(self.tab_info["tab_meta"]["cards_container"], "Nova pessoa")
                    )
                case "Tarefas":
                    self.tab_info["tab_meta"]["cards_container"].add_card(
                        CardPessoa(self.tab_info["tab_meta"]["cards_container"], "Nova pessoa")
                    )
                case "Setores":
                    self.tab_info["tab_meta"]["cards_container"].add_card(
                        CardPessoa(self.tab_info["tab_meta"]["cards_container"], "Nova pessoa")
                    )
                case "Distribuições":
                    self.tab_info["tab_meta"]["cards_container"].add_card(
                        CardPessoa(self.tab_info["tab_meta"]["cards_container"], "Nova pessoa")
                    )

            ListItemView(self.tab_info["tab_meta"]["list_container"], "Novo Registro")

            #ctk.CTkMessagebox(title="Sucesso", message=f"Pessoa {registro.id} criada!")
            self.destroy()  # fecha a janela
        except Exception as e:
            print(e)
            #ctk.CTkMessagebox(title="Erro", message=str(e))
