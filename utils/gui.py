# utils/gui.py

def center_window(window, size: tuple[int, int] = None):
    """
    Centraliza a janela `window` no monitor atual.
    Funciona com qualquer widget que implemente:
      - update_idletasks()
      - winfo_width(), winfo_height()
      - winfo_screenwidth(), winfo_screenheight()
      - geometry(...)
    """
    # Garante que geometria física esteja calculada
    window.update_idletasks()

    # Tamanho real da janela
    largura = size[0]
    altura  = size[1]

    print(largura, altura)

    # Tamanho da tela
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    print(screen_w, screen_h)

    # Calcula origem para ficar centralizado
    x = (screen_w // 2) - (largura // 2)
    y = (screen_h // 2) - (altura  // 2)

    print(x, y)

    # Aplica geometria
    window.geometry(f"{largura}x{altura}+{x}+{y}")
