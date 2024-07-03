from flask import Blueprint, render_template, request, jsonify
import io
import base64
import json
import pandas as pd
from prometheus_api_client import PrometheusConnect, MetricRangeDataFrame
from prometheus_api_client.utils import parse_datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import os

main = Blueprint('main', __name__)

PROM_URL = os.getenv('PROMETHEUS_URL', 'http://10.111.10.149:8080')

# Conexion a nuestra instancia de Prometheus
promConn = PrometheusConnect(url=PROM_URL, disable_ssl=True)

# Obtener DF Metrics Timeseries
def metric_query(labels, start_time, end_time, query):
    metric_data = promConn.get_metric_range_data(
        query,
        label_config=labels,
        start_time=start_time,
        end_time=end_time,
    )
    return MetricRangeDataFrame(metric_data)

def cargar_datos(labels, start_time, end_time, query):
    df_prom = metric_query(labels, start_time, end_time, query)
    df = df_prom[['value']].copy()
    df = df.set_index(df_prom.index)
    df = df.resample('60T').mean()

    ratio = 0.2
    size = int(len(df) * (1 - float(ratio)))
    df_train, df_test = df[0:size], df[size:len(df)]
    return df_train, df_test

def ARIMA(df_datos, steps):
    p, d, q = 0, 1, 0
    P, D, Q, m = 0, 1, 1, 12
    
    model = SARIMAX(df_datos, order=(p, d, q), seasonal_order=(P, D, Q, m), enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)

    forecast = results.get_forecast(steps=steps)
    forecast_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()
    
    return results, pd.DataFrame(forecast_values, index=confidence_intervals.index), confidence_intervals

def crear_grafico(df, forecast, confidence_intervals, query, labels):
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

def obtener_metricas():
    return promConn.all_metrics()

@main.route('/cargar_labels', methods=['POST'])
def cargar_labels():
    selected_value = request.form.get('selected_value')
    labels = promConn.get_current_metric_value(selected_value)
    metric_values = [entry['metric'] for entry in labels]
    return jsonify(metric_values)

@main.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    metricas = obtener_metricas()

    metrica = request.form.get('opciones-metrica')
    labelsObj = request.form.get('opciones-labels')
    labels = json.loads(labelsObj)
    start_time = parse_datetime("2d")
    end_time = parse_datetime("now")

    df, df_test = cargar_datos(labels, start_time, end_time, "")

    model, forecast, confidence_intervals = ARIMA(df, 24)

    img_url = crear_grafico(df, forecast, confidence_intervals, metrica, labels)
    
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=metricas)

@main.route('/')
def index():
    metricas = obtener_metricas()
    
    labels = {'job': 'node-exporter', 'instance': '10.44.0.3:9100', 'mountpoint': '/'}
    start_time = parse_datetime("2d")
    end_time = parse_datetime("now")
    query = 'node_filesystem_avail_bytes'

    df, df_test = cargar_datos(labels, start_time, end_time, query)

    model, forecast, confidence_intervals = ARIMA(df, 24)

    img_url = crear_grafico(df, forecast, confidence_intervals, query, labels)
        
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=metricas)
