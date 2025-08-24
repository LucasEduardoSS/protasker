from customtkinter import CTkFrame, CTkLabel


class SidebarBaseTabView(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent", corner_radius=0)

        self.tab_top_bar = CTkFrame(
            self,
            fg_color = "#2C2E33",
            height = 25,
            corner_radius = 0,
            border_width = 0
        )
        self.tab_top_bar.pack(side="top", fill="x")
        self.tab_top_bar.pack_propagate(False)

        self.label = CTkLabel(self.tab_top_bar, text="title", font=("Tahoma", 11))
        self.label.pack(side="left", padx=(10, 0))
