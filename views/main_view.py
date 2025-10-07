from customtkinter import CTk

from utils.gui_utils import center_window
from views.menu.menu_view import Menu
from views.workspace.workspace_view import WorkspaceView
from views.sidebar.sidebar_view import SidebarView
from views.footer.footer_view import Footer


class ProTaskerView(CTk):
    def __init__(self):
        super().__init__()
        self.title("ProTasker")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.iconbitmap("images/protasker_icon.ico")

        self.main_meta = {
            #"menu": Menu(self),
            "footer": Footer(self),
            "sidebar": SidebarView(self),
            "workspace": WorkspaceView(self)
        }
        #self.configure(menu=self.main_meta["menu"])
        self.configure(bg="#3F3F3F")

        self.main_meta["footer"].version_label.configure(text="Protasker v0.8 Beta")
        self.main_meta["footer"].lang_label.configure(text="PT-BR")

        # agenda para rodar após o pack/layout
        self.after(0, center_window(self, (1200, 700)))
