import os
import io
import pandas as pd
import base64
import matplotlib.pyplot as plt

from prometheus_api_client import PrometheusConnect, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX


class PrometheusMetrics:
    def __init__(self) -> None:
        self.promUrl = os.getenv('PROMETHEUS_URL', 'http://10.111.10.149:8080')
        self.promConn = PrometheusConnect(url=self.promUrl, disable_ssl=True)
        
    def get_current_metric_value(self, value):
        return self.promConn.get_current_metric_value(value)

    def get_all_metrics(self):
        return self.promConn.all_metrics()
    
    def get_report(self, metric, labels, start_time="2d", end_time="now"):
        start_time = parse_datetime(start_time)
        end_time = parse_datetime(end_time)

        df, df_test = self.load_data(labels, start_time, end_time, "")
        model, forecast, confidence_intervals = self.ARIMA(df, 24)

        img_url = self.crear_grafico(df, forecast, confidence_intervals, metric, labels)

        return df, img_url
    

    # Obtener DF Metrics Timeseries
    def metric_query(self, labels, start_time, end_time, query):
        metric_data = self.promConn.get_metric_range_data(
            query,
            label_config=labels,
            start_time=start_time,
            end_time=end_time,
        )
        return MetricRangeDataFrame(metric_data)

    def load_data(self, labels, start_time, end_time, query):
        df_prom = self.metric_query(labels, start_time, end_time, query)
        df = df_prom[['value']].copy()
        df = df.set_index(df_prom.index)
        df = df.resample('60T').mean()

        ratio = 0.2
        size = int(len(df) * (1 - float(ratio)))
        df_train, df_test = df[0:size], df[size:len(df)]
        return df_train, df_test

    def ARIMA(self, df_datos, steps):
        p, d, q = 0, 1, 0
        P, D, Q, m = 0, 1, 1, 12
        
        model = SARIMAX(df_datos, order=(p, d, q), seasonal_order=(P, D, Q, m), enforce_stationarity=False, enforce_invertibility=False)
        results = model.fit(disp=False)

        forecast = results.get_forecast(steps=steps)
        forecast_values = forecast.predicted_mean
        confidence_intervals = forecast.conf_int()
        
        return results, pd.DataFrame(forecast_values, index=confidence_intervals.index), confidence_intervals


    def crear_grafico(self, df, forecast, confidence_intervals, query, labels):
        plt.figure(figsize=(18, 10))
        plt.plot(df, label='Datos Históricos')
        plt.plot(forecast, color='red', label='Pronóstico')
        plt.fill_between(
            confidence_intervals.index, 
            confidence_intervals['lower value'],  
            confidence_intervals['upper value'], 
            color='pink', alpha=0.3, label='Intervalo de Confianza'
        )
        plt.xlabel('Fecha')
        plt.ylabel(query)
        plt.title(labels)
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        img_url = f'data:image/png;base64,{img_base64}'
        
        return img_url