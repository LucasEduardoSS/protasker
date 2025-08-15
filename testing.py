import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Resizable Split Frames")
        self.geometry("800x600")

        # Create the PanedWindow (horizontal)
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Left frame
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.paned.add(self.left_frame, weight=1)

        # Right frame
        self.right_frame = ctk.CTkFrame(self, width=500)
        self.paned.add(self.right_frame, weight=3)

        # Add sample widgets
        ctk.CTkLabel(self.left_frame, text="Left Frame").pack(padx=10, pady=10)
        ctk.CTkLabel(self.right_frame, text="Right Frame").pack(padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
