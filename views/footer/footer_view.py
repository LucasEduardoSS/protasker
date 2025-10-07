from customtkinter import CTkFrame, CTkLabel


class Footer(CTkFrame):
    """ Define a barra de rodapé. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2C2E33", bg_color="#3F3F3F", corner_radius=0, height=20)
        self.pack(side="bottom", fill="x", padx=0, pady=0)

        self.version_label = CTkLabel(self, text="", font=("Tahoma", 11))
        self.version_label.pack(side="right", padx=10)

        self.lang_label = CTkLabel(self, text="", font=("Tahoma", 11))
        self.lang_label.pack(side="right", padx=10)
