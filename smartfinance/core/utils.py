def format_currency(value: float) -> str:
    """Formata um número float como moeda brasileira."""
    return f"R$ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
