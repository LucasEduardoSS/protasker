import os
import platform
from pathlib import Path
from peewee import SqliteDatabase


def get_database_path(app_name: str = "ProTasker") -> Path:
    """
    Retorna o Path completo para o arquivo .db, criando a pasta se necessário.
    Em Windows usa %APPDATA%, em Linux/mac usa ~/.local/share/<app_name>.
    """
    system = platform.system()
    if system == "Windows":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData/Roaming"))
    else:
        base = Path.home() / ".local" / "share"

    app_dir = base / app_name
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir / f"{app_name.lower()}.db"

# obtém o caminho configurado
DB_PATH = get_database_path()

# instancia o banco com pragmas recomendadas
database = SqliteDatabase(
    DB_PATH,
    pragmas={
        "foreign_keys": 1,      # ativa chaves estrangeiras
        "journal_mode": "wal",  # melhor desempenho concorrente
        "cache_size": -1024 * 64
    }
)
