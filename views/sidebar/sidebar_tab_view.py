import customtkinter as ctk


class SidebarTabView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            width=100,
            fg_color="#2E333C",
            border_width=0
        )

        self.current_tab: str = ''
        self.tabs = {}
        self.setup_tabs()

    def setup_tabs(self):
        # Criar os frames para cada aba
        self.tabs = {
            "controle": self.create_tab_control(),
            "detalhes": self.create_tab_details()
        }

    def create_base_tab(self, title: str):
        frame = ctk.CTkFrame(
            self,
            fg_color="#2E333C"
        )

        tab_top_bar = ctk.CTkFrame(
            frame,
            fg_color="#2C2E33",
            height=25,
            corner_radius=0,
            border_width=0
        )
        tab_top_bar.pack(side="top", fill="x")
        tab_top_bar.pack_propagate(False)

        label = ctk.CTkLabel(tab_top_bar, text=title, font=("Tahoma", 11))
        label.pack(side="left", padx=(10, 0))

        return frame

    def create_tab_details(self):
        frame = self.create_base_tab("Detalhes")
        return frame

    def create_tab_control(self):
        frame = self.create_base_tab("Controle")
        return frame

    def show_tab(self, tab_id):
        """ Mostra a aba selecionada. Funciona como uma extensão
        da funçao toggle_sidebar_tabs neste escopo. """

        # Esconde a aba atual se existir
        if self.current_tab:  # and self.tabs[self.current_tab].winfo_ismapped()
            self.tabs[self.current_tab].pack_forget()

        # Mostra a nova aba
        self.current_tab = tab_id
        self.tabs[tab_id].pack(fill="both", expand=True)
