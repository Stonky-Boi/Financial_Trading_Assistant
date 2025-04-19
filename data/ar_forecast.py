import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
import matplotlib.pyplot as plt

def ar_forecast(series, lags=5, steps=10):
    model = AutoReg(series, lags=lags, old_names=False)
    model_fit = model.fit()
    forecast = model_fit.predict(start=len(series), end=len(series)+steps-1, dynamic=False)
    return forecast, model_fit

def plot_forecast(series, forecast):
    plt.figure(figsize=(10,5))
    plt.plot(series.index, series.values, label='Historical')
    forecast_index = pd.date_range(series.index[-1], periods=len(forecast)+1, freq='B')[1:]
    plt.plot(forecast_index, forecast, label='Forecast', color='red')
    plt.legend()
    plt.title('AR Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.tight_layout()
    return plt
