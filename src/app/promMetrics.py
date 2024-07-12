"""
Prometheus Metrics Visualizer and Forecaster

This module provides functionality to interact with a Prometheus server,
retrieve metrics data, and generate reports and visualizations.

Author: martiroman
"""

import os
from . import report
from prometheus_api_client.utils import parse_datetime
from prometheus_api_client import PrometheusConnect, MetricRangeDataFrame

class PrometheusMetrics:
    def __init__(self) -> None:
        """
        Initialize the PrometheusMetrics class.
        
        Sets up the Prometheus connection using the URL from the environment variable
        'PROMETHEUS_URL' or a default value if not set. Also initializes the report module.
        """
        self.promUrl = os.getenv('PROMETHEUS_URL', 'http://10.111.10.149:8080')
        self.promConn = PrometheusConnect(url=self.promUrl, disable_ssl=True)
        self.report = report.Report()    

    def get_report(self):
        return self.report.get_report()
        
    def generate_report(self, metric, labels, start_time="2d", end_time="now"):
        """
        Generate a report for the given metric and labels over the specified time range.
        
        Args:
            metric (str): The name of the metric.
            labels (dict): The labels to filter the metric data.
            start_time (str): The start time for the query (default is "2d" for 2 days ago).
            end_time (str): The end time for the query (default is "now").
        
        Returns:
            Timeseries data (Dataframe)
            Image URl
        """
        df_prom = self.metric_query(labels, parse_datetime(start_time), parse_datetime(end_time), "")
        df, img_url = self.report.generate_report(df_prom, metric, labels)
        return df, img_url

    def get_current_metric_value(self, value):
        """
        Retrieve the current value of a specific metric.
        
        Args:
            value (str): The name of the metric.
        
        Returns:
            The current value of the metric.
        """
        return self.promConn.get_current_metric_value(value)

    def get_labels(self, metric):
        """
        Get the labels for a specific metric.
        
        Args:
            metric (str): The name of the metric.
        
        Returns:
            A list of labels associated with the metric.
        """
        labels = self.get_current_metric_value(metric)
        metric_values = [entry['metric'] for entry in labels]
        return metric_values
    
    def get_all_metrics(self):
        """
        Retrieve all available metrics from Prometheus.
        
        Returns:
            A list of all available metrics.
        """
        return self.promConn.all_metrics()

    def metric_query(self, labels, start_time, end_time, query):
        """
        Perform a query to retrieve timeseries data for the given labels and time range.
        
        Args:
            labels (dict): The labels to filter the metric data.
            start_time (datetime): The start time for the query.
            end_time (datetime): The end time for the query.
            query (str): The Prometheus query.
        
        Returns:
            MetricRangeDataFrame: A DataFrame containing the timeseries data.
        """
        metric_data = self.promConn.get_metric_range_data(
            query,
            label_config=labels,
            start_time=start_time,
            end_time=end_time,
        )
        return MetricRangeDataFrame(metric_data)
