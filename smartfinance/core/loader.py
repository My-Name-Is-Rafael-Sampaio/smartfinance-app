import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "transactions.csv"


def load_transactions() -> pd.DataFrame:
    """Carrega as transações do arquivo CSV, criando se necessário."""
    columns = ["date", "description", "amount", "category", "card", "method", "person"]

    if not DATA_PATH.exists():
        pd.DataFrame(columns=columns).to_csv(DATA_PATH, index=False)

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    for col in columns:
        if col not in df.columns:
            df[col] = "" if col in ["method", "person"] else None
    return df[columns]


def save_transaction(date, description, amount, category, card, method, person):
    """Salva uma nova transação no CSV."""
    new_entry = pd.DataFrame(
        [
            {
                "date": pd.to_datetime(date),
                "description": description,
                "amount": float(amount),
                "category": category,
                "card": card,
                "method": method,
                "person": person,
            }
        ]
    )
    existing = load_transactions()
    updated = pd.concat([existing, new_entry], ignore_index=True)
    updated.to_csv(DATA_PATH, index=False)
