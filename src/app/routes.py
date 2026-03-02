from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import json
import os
from . import promMetrics
import warnings
warnings.filterwarnings("ignore")


main = Blueprint('main', __name__)


def get_pm():
    """
    Create a new PrometheusMetrics instance using the current configuration.
    This allows runtime changes to PROMETHEUS_URL to take effect.
    """
    return promMetrics.PrometheusMetrics()

@main.route('/getReport', methods=['GET'])
def getReport():
    
    pm = get_pm()
    df, img_url = pm.get_report()
    
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=pm.get_all_metrics())

@main.route('/getReport', methods=['POST'])
def generateReport():
    
    pm = get_pm()
    metric = request.form.get('opciones-metrica')
    labels = json.loads(request.form.get('opciones-labels'))
    df, img_url = pm.generate_report(metric, labels)
    
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=pm.get_all_metrics())

@main.route('/loadLabels', methods=['POST'])
def loadLabels():

    pm = get_pm()
    selected_value = request.form.get('selected_value')
    labels = pm.get_labels(selected_value)
    
    return jsonify(labels)

@main.route('/')
def index():
    pm = get_pm()
    return render_template('index.html', tables=[], titles="", img_url="", valores=pm.get_all_metrics())


@main.route('/config', methods=['GET', 'POST'])
def config():
    """
    Simple configuration screen to set Prometheus URL and default range.
    Changes are stored in environment variables for the current process.
    """
    default_prom_url = os.getenv('PROMETHEUS_URL', 'http://10.111.10.149:8080')
    default_range_start = os.getenv('PROM_RANGE_START', '2d')

    if request.method == 'POST':
        prom_url = request.form.get('prom_url') or default_prom_url
        prom_range_start = request.form.get('prom_range_start') or default_range_start

        os.environ['PROMETHEUS_URL'] = prom_url
        os.environ['PROM_RANGE_START'] = prom_range_start

        # After saving, redirect back to main screen
        return redirect(url_for('main.index'))

    return render_template(
        'config.html',
        prom_url=default_prom_url,
        prom_range_start=default_range_start,
    )
