import pandas as pd
from datetime import datetime
from smartfinance.config.loader import load_config


def calculate_available_budget(df: pd.DataFrame) -> dict:
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    try:
        cards_config = load_config("cards.json")
    except FileNotFoundError:
        return {"error": "cards.json not found."}

    budget = {}

    for card_name, config in cards_config.items():
        closing_day = config["closing_day"]

        if today.day <= closing_day:
            start = pd.Timestamp(
                year=current_year, month=current_month - 1, day=closing_day + 1
            )
            end = pd.Timestamp(year=current_year, month=current_month, day=closing_day)
        else:
            start = pd.Timestamp(
                year=current_year, month=current_month, day=closing_day + 1
            )
            end = pd.Timestamp(
                year=current_year + (current_month == 12),
                month=(current_month % 12) + 1,
                day=closing_day,
            )

        card_df = df[
            (df["card"] == card_name) & (df["date"] >= start) & (df["date"] <= end)
        ]
        total_spent = card_df["amount"].sum()

        budget[card_name] = {
            "billing_period_start": str(start.date()),
            "billing_period_end": str(end.date()),
            "total_spent": round(float(total_spent), 2),
        }

    return budget
