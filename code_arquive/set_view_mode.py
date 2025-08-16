
def set_view_mode(self, tab_name: str, mode: str):
    """Alterna entre 'Cards' e 'Lista' programaticamente."""
    meta = self.tabs_meta.get(tab_name)
    if not meta:
        raise ValueError(f"Tab '{tab_name}' não encontrada.")

    mode = mode.capitalize()
    if mode not in ("Cards", "Lista"):
        raise ValueError("mode deve ser 'Cards' ou 'Lista'.")

    if mode == "Cards":
        meta["list_container"].pack_forget()
        meta["cards_container"].pack(fill="both", expand=True)
    else:
        meta["cards_container"].pack_forget()
        meta["list_container"].pack(fill="both", expand=True)

    meta["view_mode"] = mode
    if meta["view_switch"] is not None:
        meta["view_switch"].set(mode)


def get_cards_container(self, tab_name: str):
    meta = self.tabs_meta.get(tab_name)
    if not meta:
        raise ValueError(f"Tab '{tab_name}' não encontrada.")
    return meta["cards_container"]


def get_list_container(self, tab_name: str):
    meta = self.tabs_meta.get(tab_name)
    if not meta:
        raise ValueError(f"Tab '{tab_name}' não encontrada.")
    return meta["list_container"]
