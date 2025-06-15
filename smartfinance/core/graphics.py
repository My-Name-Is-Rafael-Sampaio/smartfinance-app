import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from smartfinance.config.labels import category_labels
from smartfinance.core.utils import format_currency


def plot_expenses_by_category(df: pd.DataFrame):
    if df.empty or "category" not in df.columns or "amount" not in df.columns:
        fig, ax = plt.subplots()
        ax.text(
            0.5,
            0.5,
            "Nenhum dado disponível",
            horizontalalignment="center",
            verticalalignment="center",
        )
        ax.axis("off")
        return fig

    grouped = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    grouped.index = [category_labels.get(cat, cat) for cat in grouped.index]

    fig, ax = plt.subplots()
    grouped.plot(kind="bar", ax=ax)

    ax.set_title("Despesas por Categoria")
    ax.set_ylabel("Valor (R$)")
    ax.set_xlabel("Categoria")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"{format_currency(x)}")
    )

    return fig
