from data.ar_forecast import ar_forecast

def analyze_technical(df):
    close = df['C']
    forecast, model_fit = ar_forecast(close)
    reasoning = f"AR model (lags={model_fit.k_ar}) shows forecasted trend: {forecast.values.round(2)}"
    return {
        "forecast": forecast,
        "reasoning": reasoning
    }
