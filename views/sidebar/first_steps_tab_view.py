from customtkinter import CTkFrame, CTkLabel
from views.sidebar.sidebar_base_tab_view import SidebarBaseTabView


class FirstStepsTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label.configure(text="Primeiros passos")

        boas_vindas_label = CTkLabel(
            self,
            text="Bem vindo ao ProTasker!",
            font=("Tahoma", 11),
            fg_color="transparent"
        )
        boas_vindas_label.pack(
            anchor="center",
            pady=(50, 0),
            side="top"
        )

        primeiros_passos_frame = CTkFrame(
            self,
            fg_color="transparent",
            width=200
        )
        primeiros_passos_frame.pack(
            anchor="center",
            side="top",
            pady=(20, 0)
        )
        primeiros_passos_frame.grid_propagate(False)

        primeiros_passos_label = CTkLabel(
            primeiros_passos_frame,
            text="Primeiros passos:",
            font=("Tahoma", 11),
            fg_color="transparent"
        )
        primeiros_passos_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(20, 0)
        )

        passo_criar_setor = CTkLabel(
            primeiros_passos_frame,
            text="1. Registre um setor (opcional).",
            font=("Tahoma", 11),
            fg_color="transparent"
        )
        passo_criar_setor.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(20, 0)
        )
        # passo1_label.bind("<Button-1>", lambda _: self.master.show_view("login"))

        passo_criar_pessoa = CTkLabel(
            primeiros_passos_frame,
            text="2. Registre uma pessoa.",
            font=("Tahoma", 11),
            fg_color="transparent"
        )
        passo_criar_pessoa.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(20, 0)
        )

        passo_criar_tarefa = CTkLabel(
            primeiros_passos_frame,
            text="3. Registre uma tarefa.",
            font=("Tahoma", 11),
            fg_color="transparent"
        )
        passo_criar_tarefa.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(20, 0)
        )

        passo_gerar_distro = CTkLabel(
            primeiros_passos_frame,
            text="4. Gere uma distribuição.",
            font=("Tahoma", 11),
            fg_color="transparent"
        )
        passo_gerar_distro.grid(
            row=4,
            column=0,
            sticky="w",
            padx=(20, 0)
        )
