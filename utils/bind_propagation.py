
def propagate_hover_bind(p_widget, hover_fg: str, normal_fg: str = None):
    """
    Propaga hover para widgets filhos.
    Por padrão, a cor dos widgets filhos volta para transparent.
    """

    def _on_hover_enter(widget):
        """Troca a cor do frame ao passar o mouse."""
        widget.configure(fg_color=hover_fg)

    def _on_hover_leave(widget):
        """Restaura a cor normal do frame quando o mouse sai."""
        widget.configure(fg_color=normal_fg if normal_fg else "transparent")

    # Hover leve (evita mudança contínua em <Motion>)
    p_widget.bind("<Enter>", lambda e: _on_hover_enter(p_widget), add="+")
    p_widget.bind("<Leave>", lambda e: _on_hover_leave(p_widget), add="+")

    for child in p_widget.winfo_children():
        child.bind("<Enter>", lambda e: _on_hover_enter(p_widget), add="+")
        child.bind("<Leave>", lambda e: _on_hover_leave(p_widget), add="+")

        if hasattr(child, "winfo_children"):
            for subchild in child.winfo_children():
                subchild.bind("<Enter>", lambda e: _on_hover_enter(p_widget), add="+")
                subchild.bind("<Leave>", lambda e: _on_hover_leave(p_widget), add="+")
