import streamlit as st
from smartfinance.core.loader import load_transactions, save_transaction
from smartfinance.core.calculator import calculate_available_budget
from smartfinance.core.graphics import plot_expenses_by_category
from smartfinance.core.alerts import generate_alerts
from smartfinance.config.loader import load_config
from smartfinance.config.labels import category_labels, payment_labels
from smartfinance.core.utils import format_currency
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="SmartFinance", layout="wide")
st.title("\U0001F4CA SmartFinance – Assistente Financeiro Pessoal")

if st.session_state.get("success"):
    st.success("✅ Transação adicionada com sucesso!")
    st.session_state["success"] = False

data = load_transactions()

# --- Nova Transação ---
tabs = st.sidebar.radio("Menu", ["Nova Transação", "Painel"])

if tabs == "Nova Transação":
    st.sidebar.header("➕ Nova Transação")
    date = st.sidebar.date_input("Data", datetime.today(), format="DD/MM/YYYY")
    description = st.sidebar.text_input("Descrição")
    amount = st.sidebar.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    categories = load_config("categories.json")
    translated_categories = [category_labels.get(c, c) for c in categories]
    category_display = st.sidebar.selectbox("Categoria", translated_categories)
    category = next((k for k, v in category_labels.items() if v == category_display), category_display)

    methods = load_config("payment_methods.json")
    translated_methods = [payment_labels.get(m, m) for m in methods]
    method_display = st.sidebar.selectbox("Forma de Pagamento", translated_methods)
    method = next((k for k, v in payment_labels.items() if v == method_display), method_display)

    card = ""
    if method in ["Credit", "Debit"]:
        cards = list(load_config("cards.json").keys())
        card = st.sidebar.selectbox("Cartão", cards)
    elif method == "Pix":
        pix_by_card = st.sidebar.checkbox("Feito via Cartão de Crédito?")
        if pix_by_card:
            cards = list(load_config("cards.json").keys())
            card = st.sidebar.selectbox("Cartão", cards)

    person = st.sidebar.text_input("Responsável")

    if st.sidebar.button("Adicionar"):
        if not description.strip():
            st.sidebar.error("Descrição é obrigatória.")
        elif amount <= 0:
            st.sidebar.error("O valor deve ser maior que zero.")
        elif not category:
            st.sidebar.error("Categoria é obrigatória.")
        elif not method:
            st.sidebar.error("Forma de pagamento é obrigatória.")
        elif method in ["Credit", "Debit"] and not card:
            st.sidebar.error("Selecione um cartão válido.")
        elif not person.strip():
            st.sidebar.error("Responsável é obrigatório.")
        else:
            save_transaction(date, description, amount, category, card, method, person)
            st.session_state["success"] = True
            st.rerun()

# --- Painel ---
else:
    st.subheader("⚠️ Alertas")
    for alert in generate_alerts(data, category_labels):
        st.warning(alert)

    st.subheader("💼 Visão Geral das Transações")

    if not data.empty:
        total_spent = data["amount"].sum()
        st.markdown(f"### 💰 Gasto Total: **{format_currency(total_spent)}**")

        translated_data = data.copy()
        translated_data["category"] = translated_data["category"].map(category_labels).fillna(translated_data["category"])
        translated_data["method"] = translated_data["method"].map(payment_labels).fillna(translated_data["method"])
        translated_data["date"] = pd.to_datetime(translated_data["date"], errors="coerce", dayfirst=True).dt.strftime("%d/%m/%Y")

        for idx, row in data.iterrows():
            with st.expander(f"📌 {row['description']} | {row['date'].strftime('%d/%m/%Y')} | 💵 {format_currency(row['amount'])}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📅 Data:** {row['date'].strftime('%d/%m/%Y')}")
                    st.markdown(f"**📂 Categoria:** {category_labels.get(row['category'], row['category'])}")
                    st.markdown(f"**💳 Forma de Pagamento:** {payment_labels.get(row['method'], row['method'])}")
                    st.markdown(f"**🏦 Cartão:** {row['card'] if pd.notna(row['card']) else '—'}")
                with col2:
                    st.markdown(f"**👤 Responsável:** {row['person']}")
                    st.markdown(f"**💰 Valor:** {format_currency(row['amount'])}")
                    if st.button("🗑️ Remover", key=f"delete_{idx}"):
                        df = load_transactions()
                        df.drop(index=idx, inplace=True)
                        df.to_csv("smartfinance/data/transactions.csv", index=False)
                        st.success("Transação removida com sucesso!")
                        st.rerun()
    else:
        st.info("Nenhuma transação registrada ainda.")

    st.subheader("📉 Orçamento Disponível")
    budget = calculate_available_budget(data)
    for card, info in budget.items():
        start = datetime.strptime(info["billing_period_start"], "%Y-%m-%d").strftime("%d/%m/%Y")
        end = datetime.strptime(info["billing_period_end"], "%Y-%m-%d").strftime("%d/%m/%Y")
        st.markdown(f"**💳 Cartão:** {card}")
        st.markdown(f"- 📆 Período da fatura: **{start}** até **{end}**")
        st.markdown(f"- 💸 Total gasto no período: **{format_currency(info['total_spent'])}**")
        st.markdown("---")

    st.subheader("📊 Despesas por Categoria")
    fig = plot_expenses_by_category(data)
    st.pyplot(fig)

st.caption("Desenvolvido por Rafael Sampaio • Versão 0.1")
