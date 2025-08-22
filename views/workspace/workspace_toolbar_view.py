from customtkinter import CTkFrame
from views.components.toolbar_buttons_view import ViewModeSwitch, AddButton, FilterButton


class WorkspaceToolbarView(CTkFrame):
    """ Define a barra de ferramentas para as tabs do workspace. """

    def __init__(self, master, tab_name, **kwargs):
        super().__init__(master, **kwargs)

        self.tab_info = {
            "tab_name": tab_name,
            "tab_master": master.master,  # WorkspaceTabView
            "tab_meta": master.master.tabs_meta[tab_name]
        }

        self.configure(
            height=35,
            corner_radius=5,
            border_width=1,
            border_color="#555"
        )

        self.pack(side="top", fill="x", padx=5, pady=4)
        self.pack_propagate(False)

        # Lado esquerda da toolbar
        self.toolbar_left = CTkFrame(self, fg_color="transparent")
        self.toolbar_left.pack(side="left", padx=2, pady=2, anchor="w")

        # Espaçamento central
        self.spacer = CTkFrame(self, fg_color="transparent")
        self.spacer.pack(side="left", padx=2, pady=2, fill="x", expand=True)

        # Lado direito da toolbar
        self.toolbar_right = CTkFrame(self, fg_color="transparent")
        self.toolbar_right.pack(side="right", padx=2, pady=2, anchor="w")

        self.add = AddButton(self.toolbar_left, tab_info=self.tab_info)
        self.filter = FilterButton(self.toolbar_left, tab_info=self.tab_info)
        self.view_mode_switch = ViewModeSwitch(self.toolbar_right, tab_info=self.tab_info)
