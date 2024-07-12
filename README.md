# Prometheus Timeseries Metrics Visualizer and Forecaster

This project is a web application written in Python that allows users to select a Prometheus metric, visualize it with a graph, and perform forecasting.
Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/martiroman/timeseries-forecasting.git
    cd timeseries-forecasting
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r src/requirements.txt
    ```
## Configuration

To configure the Prometheus URL, modify the PROMETHEUS_URL variable in the .env file.

        PROMETHEUS_URL=http://10.111.10.149:8080
        DEBUG=True

Usage

1. Start the application:
    ```bash
    python src/run.py
    ```

2. Open your browser and go to `http://localhost:5000`.

3. Select a Prometheus metric from the dropdown menu.

## ARIMA Model

ARIMA (Autoregressive Integrated Moving Average) is a statistical model used to analyze and forecast time series data. It can be fitted to historical data to make future predictions, making it valuable for forecasting variables in various disciplines.

We use SARIMAX, an extension of the model that considers external factors or exogenous variables.

Doc: https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html