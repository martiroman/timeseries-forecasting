# Prometheus Timeseries Metrics Visualizer and Forecaster

Este proyecto es una aplicación web escrita en Python que permite a los usuarios seleccionar una métrica de Prometheus, visualizarla mediante un gráfico y realizar un pronóstico (forecasting).

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/martiroman/timeseries-forecasting.git
    cd timeseries-forecasting
    ```

2. Crea un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r src/requirements.txt
    ```
## Configuración

Para configurar la URL de Prometheus, modifica la variable `PROMETHEUS_URL` en el archivo `.env`.

        PROMETHEUS_URL=http://10.111.10.149:8080
        DEBUG=True

## Uso

1. Inicia la aplicación:
    ```bash
    python src/run.py
    ```

2. Abre tu navegador y ve a `http://localhost:5000`.

3. Selecciona una métrica de Prometheus desde el menú desplegable.

## Modelo ARIMA

ARIMA (Autoregressive Integrated Moving Average) es un modelo estadístico utilizado para analizar y predecir series temporales. Puede ser ajustado a datos históricos para hacer predicciones a futuro, lo que lo hace valioso en pronósticos de variables en distintas disciplinas.

Utilizamos SARIMAX, una extensión del modelo que considera factores externos o variables exógenas.

Doc: https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html