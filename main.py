import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator

st.set_page_config(page_title="Dashboard de Ações", layout="wide")

# =============================
# 🔧 Funções auxiliares
# =============================

def calcular_mme(df, periodos):
    for p in periodos:
        df[f'MME_{p}'] = df['Close'].ewm(span=p, adjust=False).mean()
    return df

def calcular_ifr(df, periodo=14):
    close = df['Close']
    rsi = RSIIndicator(close=pd.Series(close), window=periodo)
    df['IFR'] = rsi.rsi()
    return df


def calcular_obv(df):
    close = df['Close']
    volume = df['Volume']
    obv_indicator = OnBalanceVolumeIndicator(close=close, volume=volume)
    df['OBV'] = obv_indicator.on_balance_volume()
    return df


def calcular_didi(df):
    df['Didi_Curta'] = df['Close'].ewm(span=3, adjust=False).mean()
    df['Didi_Media'] = df['Close'].ewm(span=8, adjust=False).mean()
    df['Didi_Longa'] = df['Close'].ewm(span=20, adjust=False).mean()
    return df


def calcular_fibonacci(ponto_a, ponto_b):
    distancia = ponto_b - ponto_a
    nivel_0 = ponto_b
    nivel_100 = ponto_a
    nivel_1alvo = ponto_b + distancia
    nivel_161 = ponto_b + distancia * 1.618
    return nivel_0, nivel_100, nivel_1alvo, nivel_161


def resample_data(df, timeframe):
    df = df.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    ohlc_dict = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }

    if timeframe == 'Mensal':
        df_resampled = df.resample('ME').agg(ohlc_dict)
    elif timeframe == 'Semanal':
        df_resampled = df.resample('W').agg(ohlc_dict)
    else:
        df_resampled = df

    df_resampled = df_resampled.dropna()

    return df_resampled

# =============================
# 🎨 Interface
# =============================

st.sidebar.title("Ajustes")

ticker = st.sidebar.text_input("Ticker (ex: PETR4.SA, AAPL, BTC-USD)", "PETR4.SA").upper()
timeframe = st.sidebar.selectbox("Timeframe", ["Mensal", "Semanal", "Diário"])
data_inicio = st.sidebar.date_input("Data inicial", pd.to_datetime('2010-01-01'))
data_fim = st.sidebar.date_input("Data final", pd.to_datetime('today'))

# 🔢 Projeção de Fibonacci
ponto_b = st.sidebar.number_input("Ponto B (Topo)", value=0.0)
ponto_a = st.sidebar.number_input("Ponto A (Fundo)", value=0.0)

# ⚙️ Calcula os níveis de Fibonacci
fib_0, fib_100, fib_1alvo, fib_161 = calcular_fibonacci(ponto_a, ponto_b)

st.sidebar.markdown(f"""
**Primeiro Alvo - 100%:** `{fib_1alvo:.2f}`
""")
st.sidebar.markdown(f"""
**Segundo Alvo - 161,8%:** `{fib_161:.2f}`
""")

# =============================
# 🚀 Download dos Dados
# =============================

st.title(f"📊 Análise Gráfica - {ticker}")

df = yf.download(ticker, start=data_inicio, end=data_fim, progress=False)

# 🔥 Correção para colunas multi-index (yfinance às vezes retorna assim)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para esse ticker.")
    st.stop()

df.index = pd.to_datetime(df.index)

if timeframe != 'Diário':
    df = resample_data(df, timeframe)

if 'Close' not in df.columns:
    st.error("❌ Dados não possuem coluna 'Close'. Verifique o ticker ou o período selecionado.")
    st.stop()

df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

# =============================
# 🧠 Cálculo dos Indicadores
# =============================

df = calcular_mme(df, [9, 21, 144])
df = calcular_obv(df)
df = calcular_didi(df)
df = calcular_ifr(df)

fib_0, fib_100, fib_1alvo, fib_161 = calcular_fibonacci(ponto_a, ponto_b)

# =============================
# 📊 Abas de Conteúdo
# =============================

aba1, aba2, aba3 = st.tabs(["📈 Gráfico Principal", "📉 Indicadores", "📄 Dados"])

# 📈 Gráfico Principal
with aba1:
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candles'
    ))

    fig.add_trace(go.Scatter(
        x=df.index, y=df['MME_9'], mode='lines', name='MME 9', line=dict(color='blue')))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MME_21'], mode='lines', name='MME 21', line=dict(color='orange')))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MME_144'], mode='lines', name='MME 144', line=dict(color='grey')))

    # Fibonacci
    fig.add_hline(y=fib_0, line_dash="dot", line_color="green", annotation_text="0%")
    fig.add_hline(y=fib_100, line_dash="dot", line_color="red", annotation_text="-100%")
    fig.add_hline(y=fib_1alvo, line_dash="dot", line_color="orange", annotation_text="100%")
    fig.add_hline(y=fib_161, line_dash="dot", line_color="gold", annotation_text="161.8%")

    fig.update_layout(title=f"{ticker} - {timeframe}",
                      xaxis_rangeslider_visible=False,
                      height=700)

    st.plotly_chart(fig, use_container_width=True)

# 📉 Indicadores Secundários
with aba2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔋 OBV")
        fig_obv = go.Figure()
        fig_obv.add_trace(go.Scatter(
            x=df.index, y=df['OBV'], mode='lines', name='OBV', line=dict(color='green')))
        fig_obv.update_layout(
            height=300,
            title="On Balance Volume (OBV)",
            xaxis_title="Data",
            yaxis_title="OBV"
        )
        st.plotly_chart(fig_obv, use_container_width=True)

    with col2:
        st.subheader("💎 IFR (14)")
        fig_ifr = go.Figure()
        fig_ifr.add_trace(go.Scatter(
            x=df.index, y=df['IFR'], mode='lines', name='IFR', line=dict(color='orange')))
        fig_ifr.update_layout(
            height=300,
            title="Índice de Força Relativa (IFR)",
            xaxis_title="Data",
            yaxis_title="IFR",
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig_ifr, use_container_width=True)

    st.subheader("🎯 Agulhada do Didi")
    fig_didi = go.Figure()
    fig_didi.add_trace(go.Scatter(
        x=df.index, y=df['Didi_Curta'], mode='lines', name='Curta (3)', line=dict(color='blue')))
    fig_didi.add_trace(go.Scatter(
        x=df.index, y=df['Didi_Media'], mode='lines', name='Média (8)', line=dict(color='orange')))
    fig_didi.add_trace(go.Scatter(
        x=df.index, y=df['Didi_Longa'], mode='lines', name='Longa (20)', line=dict(color='grey')))
    fig_didi.update_layout(
        height=400,
        title="Agulhada do Didi",
        xaxis_title="Data",
        yaxis_title="Preço"
    )
    st.plotly_chart(fig_didi, use_container_width=True)

# 📄 Dados Tabulares
with aba3:
    st.subheader("📄 Dados")
    st.dataframe(df)
