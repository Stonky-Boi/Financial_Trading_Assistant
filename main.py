import streamlit as st
from data.data_loader import get_yfinance_data, get_fundamental_data_yf
from agents.fundamental_agent import analyze_fundamentals
from agents.technical_agent import analyze_technical
from agents.sentiment_agent import aggregate_sentiment
from agents.risk_agent import assess_risk
from agents.supervisor_agent import make_decision
from data.ar_forecast import plot_forecast
from utils.plot_utils import st_plot_matplotlib

st.title("Multi-Agent Financial Trading Assistant")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")

if st.button("Analyze"):
    # Data Parsing
    st.header("Parsing")
    df = get_yfinance_data(ticker)
    st.write(df.tail())

    fundamental_data = get_fundamental_data_yf(ticker)
    st.write(fundamental_data)

    # Agent Analyses
    st.header("Agent Analyses")
    st.subheader("Fundamental Analysis")
    fundamental_result = analyze_fundamentals(fundamental_data, ticker)
    st.write(fundamental_result)

    st.subheader("Technical Analysis & AR Forecast")
    technical_result = analyze_technical(df)
    st.write(technical_result["reasoning"])
    plt = plot_forecast(df['C'], technical_result["forecast"])
    st_plot_matplotlib(plt)

    st.subheader("Sentiment Analysis")
    sentiment_result = aggregate_sentiment(ticker)
    st.write(sentiment_result)

    st.subheader("Risk Assessment")
    risk_result = assess_risk(fundamental_result, technical_result["reasoning"], sentiment_result, ticker)
    st.write(risk_result)

    # Supervisor/Trader Decision
    st.header("Final Recommendation")
    decision = make_decision(fundamental_result, technical_result["reasoning"], sentiment_result, risk_result, ticker)
    st.write(decision)
