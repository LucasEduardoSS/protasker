'''def _resolve_sector(fields: Dict[str, Any]) -> Any:
    """
    Retorna o melhor valor para "Setor" a partir dos campos disponíveis.
    Prioriza 'sector_name'. Se não houver, tenta buscar pelo ID em 'sector'.
    """
    if "sector_name" in fields and fields["sector_name"]:
        return fields["sector_name"]

    # Variações que podem aparecer
    sector_id = fields.get("sector") or fields.get("setor") or fields.get("sector_id")
    if sector_id in (None, "", 0):
        return None

    # Evita consulta se o import falhou
    if Sector is None:
        return str(sector_id)

    try:
        # sector_id pode vir como int, str, ou até como objeto
        sid = sector_id.id if hasattr(sector_id, "id") else sector_id
        sector_obj = Sector.get_by_id(sid)
        return getattr(sector_obj, "name", str(sid))
    except Exception:
        return str(sector_id)'''
