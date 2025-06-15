#!/bin/bash
# Formatação automática com black

export PYTHONPATH=.
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Formatando código com black..."
black smartfinance

echo "Formatação concluída."
