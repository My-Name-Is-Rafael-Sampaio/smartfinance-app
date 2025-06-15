import streamlit as st
from smartfinance.core.loader import load_transactions, save_transaction
from smartfinance.core.calculator import calculate_available_budget
from smartfinance.core.graphics import plot_expenses_by_category
from smartfinance.core.alerts import generate_alerts
from smartfinance.config.loader import load_config
from smartfinance.config.labels import category_labels
from datetime import datetime

st.set_page_config(page_title="SmartFinance", layout="wide")
st.title("📊 SmartFinance – Assistente Financeiro Pessoal")

data = load_transactions()

tabs = st.sidebar.radio("Menu", ["Nova Transação", "Painel"])

if tabs == "Nova Transação":
    st.sidebar.header("➕ Nova Transação")
    date = st.sidebar.date_input("Data", datetime.today(), format="DD/MM/YYYY")
    description = st.sidebar.text_input("Descrição")
    amount = st.sidebar.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    categories = load_config("categories.json")
    translated_categories = [category_labels.get(c, c) for c in categories]
    category_display = st.sidebar.selectbox("Categoria", translated_categories)
    category = [k for k, v in category_labels.items() if v == category_display][0]

    cards = list(load_config("cards.json").keys())
    card = st.sidebar.selectbox("Cartão", cards)

    if st.sidebar.button("Adicionar"):
        save_transaction(date, description, amount, category, card)
        st.sidebar.success("Transação adicionada com sucesso!")
        st.rerun()

else:
    st.subheader("⚠️ Alertas")
    for alert in generate_alerts(data, category_labels):
        st.warning(alert)

    st.subheader("💼 Visão Geral das Transações")
    translated_data = data.copy()
    translated_data["category"] = (
        translated_data["category"]
        .map(category_labels)
        .fillna(translated_data["category"])
    )
    translated_data["date"] = translated_data["date"].dt.strftime("%d/%m/%Y")
    translated_data["amount"] = translated_data["amount"].map(
        lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    translated_data = translated_data.rename(
        columns={
            "date": "Data",
            "description": "Descrição",
            "amount": "Valor (R$)",
            "category": "Categoria",
            "card": "Cartão",
        }
    )
    st.dataframe(translated_data, use_container_width=True)

    st.subheader("📉 Orçamento Disponível")
    budget = calculate_available_budget(data)
    for card, info in budget.items():
        start = datetime.strptime(info["billing_period_start"], "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
        end = datetime.strptime(info["billing_period_end"], "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
        st.markdown(f"**💳 Cartão:** {card}")
        st.markdown(f"- 📆 Período da fatura: **{start}** até **{end}**")
        st.markdown(
            f"- 💸 Total gasto no período: **R$ {info['total_spent']:,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + "**"
        )
        st.markdown("---")

    st.subheader("📊 Despesas por Categoria")
    fig = plot_expenses_by_category(data)
    st.pyplot(fig)

st.caption("Desenvolvido por Rafael Sampaio • Versão 0.1")
