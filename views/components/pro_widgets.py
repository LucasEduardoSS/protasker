import customtkinter as ctk


class ProButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            font=("Tahoma", 11),
            corner_radius=5,
            border_width=0,
            fg_color="#2C2E33",
            hover_color="#3E4D66"
        )


class ProComboBox(ctk.CTkComboBox):
    def __init__(self, master, values: list, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            height=25,
            values=values,
            fg_color="#2C2E33",
            font=("Tahoma", 11),
            dropdown_font=("Tahoma", 11),
            dropdown_fg_color="#2C2E33",
            corner_radius=5
        )

        self._border_width = 0
        self._dropdown_menu.configure(
            fg_color="#2C2E33",
            font=("Tahoma", 11)
        )


class ProCheckBox(ctk.CTkCheckBox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#2C2E33",
            hover_color="#3E4D66",
            font=("Tahoma", 11),
            border_width=1,
            corner_radius=0,
            checkbox_width=20,
            checkbox_height=20
        )


class ProRadioButton(ctk.CTkRadioButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#3E4D66",
            hover_color="#3E4D66",
            font=("Tahoma", 11),
            border_width_checked=7,
            border_width_unchecked=1,
            radiobutton_width=15,
            radiobutton_height=15
        )
