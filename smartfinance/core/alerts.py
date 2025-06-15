from datetime import datetime
import pandas as pd
from smartfinance.config.loader import load_config
from smartfinance.core.utils import format_currency


def generate_alerts(df: pd.DataFrame, category_labels: dict = None) -> list[str]:
    alerts = []
    today = datetime.today()

    try:
        cards_config = load_config("cards.json")
    except FileNotFoundError:
        alerts.append("⚠️ Arquivo de configuração cards.json não encontrado.")
        return alerts

    for card, config in cards_config.items():
        closing_day = config["closing_day"]
        due_day = config["due_day"]
        closing_date = datetime(today.year, today.month, closing_day)
        due_date = datetime(today.year, today.month, due_day)

        if 0 <= (closing_date - today).days <= 3:
            alerts.append(
                f"📌 O fechamento da fatura do cartão {card} está próximo ({closing_date.strftime('%d/%m')})."
            )

        if 0 <= (due_date - today).days <= 3:
            alerts.append(
                f"💳 O vencimento da fatura do cartão {card} está próximo ({due_date.strftime('%d/%m')})."
            )

    if not df.empty:
        monthly = df[df["date"].dt.month == today.month]
        if not monthly.empty:
            grouped = monthly.groupby("category")["amount"].sum()
            top_category = grouped.idxmax()
            amount = grouped.max()
            if amount > 0.5 * monthly["amount"].sum():
                label = (
                    category_labels.get(top_category, top_category)
                    if category_labels
                    else top_category
                )
                alerts.append(
                    f"🔎 Alto gasto na categoria '{label}' este mês: {format_currency(amount)}"
                )

    if not alerts:
        alerts.append("✅ Nenhum alerta no momento. Continue assim!")

    return alerts
