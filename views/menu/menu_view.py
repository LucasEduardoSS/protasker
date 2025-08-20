import customtkinter as ctk

class Menu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#5F5F5F", corner_radius=0)
        self.pack(anchor="nw", side="top", fill="x", ipady=0, ipadx=0)

        self.add_button("Editar")
        self.add_button("Ver")
        self.add_button("Relatórios")
        self.add_button("Opções")
        self.add_button("Ajuda")

    def add_button(self, text):
        button = ctk.CTkButton(self, width=20, height=25, text=text, fg_color="#5F5F5F",
            corner_radius=0, font=("Tahoma", 11), hover_color="#2F2F2F")
        button.pack(side="left", ipadx=10, ipady=0, padx=0, pady=0, expand=False)
