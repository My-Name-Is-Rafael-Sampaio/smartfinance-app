#!/bin/bash
# Ativação do ambiente virtual e execução do app

export PYTHONPATH=.
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Iniciando aplicação Streamlit..."
streamlit run smartfinance/main.py
