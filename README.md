📊 Base OHLC + Indicadores

Este projeto é um dashboard de análise técnica de ativos financeiros, desenvolvido em Python com Streamlit. Permite visualizar gráficos de candlestick com médias móveis, OBV, IFR, Didi e projeções de Fibonacci.

🚀 Funcionalidades

🎯 Candlestick interativo com Médias Móveis (MME)

🔢 Projeção de Fibonacci

💎 IFR (Índice de Força Relativa)

🔋 OBV (On Balance Volume)

🎯 Agulhada do Didi

⌛️ Timeframes: Diário, Semanal e Mensal

🛠️ Tecnologias e bibliotecas

Python

Streamlit

yFinance

Plotly

Pandas

TA-Lib (via biblioteca ta)

🐳 Executando com Docker

Para facilitar a execução e evitar problemas de ambiente, você pode rodar este projeto dentro de um container Docker.

Crie o arquivo Dockerfile na raiz do projeto (caso ainda não exista):

Use imagem base com Python
FROM python:3.10-slim

Define diretório de trabalho
WORKDIR /app

Copia arquivos do projeto para o container
COPY . /app

Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

Expõe a porta padrão do Streamlit
EXPOSE 8501

Comando para iniciar o app
CMD ["streamlit", "run", "main.py", "--server.enableCORS=false"]

Crie o arquivo .dockerignore (opcional, mas recomendado):

venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
docs/

Construa a imagem Docker (dentro da pasta do projeto):

docker build -t plataforma-analise .

Execute o container:

docker run -p 8501:8501 plataforma-analise

Acesse no navegador:

http://localhost:8501

⚙️ Execução Local (sem Docker)

Crie e ative um ambiente virtual:

python3 -m venv venv
source venv/bin/activate

Instale as dependências:

pip install --upgrade pip
pip install -r requirements.txt

Execute o Streamlit:

streamlit run main.py
