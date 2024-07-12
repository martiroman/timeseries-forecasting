import io
import pandas as pd
import base64
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

class Report:
    def __init__(self) -> None:
        self.img_url = ""
        self.df = None
        self.df_train = None
        self.df_test = None
        self.forecast = None
        self.confidence_intervals = None
        self.title = ""
        self.labels = ""

    def get_report(self):
        return self.df_train, self.img_url
    
    def generate_report(self, df_prom, metric, labels):
        self.title = metric
        self.labels = labels
        self.load_data(df_prom)

        self.ARIMA(24)
        self.generate_graph()
        
        return self.df_train, self.img_url

    def generate_graph(self):
        plt.figure(figsize=(18, 10))
        plt.plot(self.df_train, label='Timeseries Data')
        plt.plot(self.forecast, color='red', label='Forecast')
        plt.fill_between(
            self.confidence_intervals.index, 
            self.confidence_intervals['lower value'],  
            self.confidence_intervals['upper value'], 
            color='pink', alpha=0.3, label='Intervalo de Confianza'
        )
        plt.xlabel('Fecha')
        plt.ylabel(self.labels)
        plt.title(self.title)
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        self.img_url = f'data:image/png;base64,{img_base64}'
    
    def load_data(self, df_prom):
        
        df = df_prom[['value']].copy()
        df = df.set_index(df_prom.index)
        df = df.resample('60T').mean()

        ratio = 0.2
        size = int(len(df) * (1 - float(ratio)))
        self.df_train, self.df_test = df[0:size], df[size:len(df)]

    def ARIMA(self, steps):
        p, d, q = 0, 1, 0
        P, D, Q, m = 0, 1, 1, 12
        
        model = SARIMAX(self.df_train, order=(p, d, q), seasonal_order=(P, D, Q, m), enforce_stationarity=False, enforce_invertibility=False)
        results = model.fit(disp=False)

        forecast = results.get_forecast(steps=steps)
        forecast_values = forecast.predicted_mean
        self.confidence_intervals = forecast.conf_int()
        
        self.forecast = pd.DataFrame(forecast_values, index=self.confidence_intervals.index)
