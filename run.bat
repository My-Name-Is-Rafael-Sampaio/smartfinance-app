@echo off
set PYTHONPATH=.
echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Iniciando aplicação Streamlit...
streamlit run smartfinance/main.py
pause
