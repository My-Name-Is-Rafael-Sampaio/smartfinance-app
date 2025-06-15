@echo off
set PYTHONPATH=.
echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Formatando código com black...
black smartfinance

echo Formatação concluída.
pause
