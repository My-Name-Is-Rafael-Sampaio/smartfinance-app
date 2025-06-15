import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "transactions.csv"


def load_transactions() -> pd.DataFrame:
    """Carrega as transações do arquivo CSV."""
    if DATA_PATH.exists() and DATA_PATH.stat().st_size > 0:
        return pd.read_csv(DATA_PATH, parse_dates=["date"])
    return pd.DataFrame(columns=["date", "description", "amount", "category", "card"])


def save_transaction(date, description, amount, category, card):
    """Salva uma nova transação no CSV."""
    new_entry = pd.DataFrame(
        [
            {
                "date": pd.to_datetime(date),
                "description": description,
                "amount": float(amount),
                "category": category,
                "card": card,
            }
        ]
    )
    existing = load_transactions()
    updated = pd.concat([existing, new_entry], ignore_index=True)
    updated.to_csv(DATA_PATH, index=False)
