# 💰 SmartFinance – Assistente Financeiro Pessoal

SmartFinance é um assistente financeiro pessoal inteligente e personalizável, desenvolvido em Python com Streamlit. Ele ajuda a gerenciar seu orçamento, acompanhar transações por categoria e cartão, emitir alertas sobre o ciclo das faturas e fornecer insights e relatórios.

---

## 🚀 Funcionalidades

- Adição e visualização de transações de forma prática
- Organização de despesas por categoria e cartão de crédito (Nubank & PicPay)
- Visualização do orçamento disponível com base nos ciclos de fatura
- Alertas para datas próximas de fechamento e vencimento
- Detecção de padrões de gasto e emissão de avisos
- Geração de gráficos com resumo por categoria

---

## 💠 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/smartfinance.git
   mv smartfinance smartfinance-app
   cd smartfinance-app
   ```

2. Crie o ambiente virtual:

   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:

   - No **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - No **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Execute o aplicativo:

   - **Linux/macOS**:
     ```bash
     ./run.sh
     ```
   - **Windows**:
     ```bash
     .\run.bat
     ```

6. Para formatar o código com `black`:

   - **Linux/macOS**:
     ```bash
     ./format.sh
     ```
   - **Windows**:
     ```bash
     .\format.bat
     ```

7. Para **desativar** o ambiente virtual:

   ```bash
   deactivate
   ```

> **Importante:** Certifique-se de que a pasta externa do projeto não tenha o mesmo nome do pacote interno (`smartfinance`). Renomeie-a para algo como `smartfinance-app` para evitar conflitos de importação (`ModuleNotFoundError`).

---

## 📌 Autor

Desenvolvido por **Rafael Sampaio**
