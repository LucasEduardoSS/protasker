import customtkinter as ctk

from views.menu.menu_view import Menu
from views.workspace.split_content_view import SplitContentView
from views.sidebar.sidebar_view import SidebarView


class ProTaskerView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ProTasker")
        self.geometry("1000x600")
        self.minsize(1000, 600)

        self.menu = Menu(self)
        self.configure(menu=self.menu)

        self.sidebar = SidebarView(self)
        self.split_content = SplitContentView(self)
