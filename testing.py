import tkinter as tk
from email.policy import default
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Testing")
        self.geometry("800x600")

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True)

        self.card = ctk.CTkFrame(frame, width=200, height=200, corner_radius=10, fg_color="blue")
        self.card.pack(anchor="center", side="top", pady=(20, 0))
        self.card.bind("<Enter>", lambda e: card.configure(fg_color="red", height=300))
        self.card.bind("<Leave>", lambda e: card.configure(fg_color="blue", height=200))
        self.card.pack_propagate(False)

        self.field = ctk.CTkFrame(card, height=15, fg_color="green")
        self.field.pack(side="top", anchor="center", padx=10, pady=10)
        self.field.bind("<Enter>", self.edit_field)
        self.field.bind("<Map>", lambda e: print("Map", e))

        #entry = ctk.CTkEntry(card, placeholder_text="Placeholder text")
        #entry.pack(padx=10, pady=10)
        #entry.bind("<FocusIn>", lambda e: print("Focused"))

        button = ctk.CTkButton(self)
        button.pack()
        button.bind("<Button-1>", lambda e: print("Button clicked"))

    def edit_field(e):
        print(e)
        self.card.configure(fg_color="red", height=300)
        print("Edit field")


if __name__ == "__main__":
    app = App()
    app.mainloop()
