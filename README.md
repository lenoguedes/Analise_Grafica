# Painel de análise técnica de ativos

Painel em Python e Streamlit para acompanhar ações, índices e criptomoedas: busca as cotações no Yahoo Finance, agrupa por período e calcula indicadores técnicos em gráficos interativos.

**Demo:** [abrir no Streamlit](https://i7qrvxaexuqfix4zjxrtru.streamlit.app/)

## O que dá para fazer

- Escolher o ativo (ex.: `PETR4.SA`, `AAPL`, `BTC-USD`), o período e o timeframe (diário, semanal ou mensal).
- Ver o gráfico de candles com médias móveis exponenciais.
- Informar um topo e um fundo para projetar alvos de Fibonacci (100% e 161,8%).
- Acompanhar OBV, IFR (14) e a Agulhada do Didi em abas separadas.
- Consultar a tabela com os dados tratados.

## Como os dados são tratados

1. Download das cotações diárias com `yfinance`.
2. Validação: o painel avisa quando o ticker não retorna dados ou vem sem a coluna de fechamento.
3. Reamostragem para semanal ou mensal (abertura do primeiro dia, máxima, mínima, fechamento do último dia e soma do volume).
4. Cálculo dos indicadores com `pandas` e a biblioteca `ta`.

## Como executar

Com Docker:

```bash
docker build -t analise-grafica .
docker run -p 8501:8501 analise-grafica
```

Ou localmente:

```bash
python -m venv venv
source venv/bin/activate   # no Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

Depois, acesse `http://localhost:8501`.

## Tecnologias

Python, Streamlit, yfinance, pandas, Plotly, ta e Docker.

> Projeto de estudo. Não é recomendação de investimento.
