from customtkinter import CTk

from utils.gui_utils import center_window
from views.menu.menu_view import Menu
from views.workspace.workspace_view import WorkspaceView
from views.sidebar.sidebar_view import SidebarView


class ProTaskerView(CTk):
    def __init__(self):
        super().__init__()
        self.title("ProTasker")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.iconbitmap("images/protasker_icon.ico")

        self.main_meta = {
            "menu": Menu(self),
            "sidebar": SidebarView(self),
            "workspace": WorkspaceView(self)
        }
        self.configure(menu=self.main_meta["menu"])

        # agenda para rodar após o pack/layout
        self.after(0, center_window(self, (1200, 700)))
