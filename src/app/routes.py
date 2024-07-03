from flask import Blueprint, render_template, request, jsonify
import json
from . import promMetrics

main = Blueprint('main', __name__)
pm = promMetrics.PrometheusMetrics()

@main.route('/cargar_labels', methods=['POST'])
def cargar_labels():

    selected_value = request.form.get('selected_value')
    labels = pm.get_current_metric_value(selected_value)
    metric_values = [entry['metric'] for entry in labels]
    
    return jsonify(metric_values)

@main.route('/generar_reporte', methods=['POST'])
def generar_reporte():
    
    metric = request.form.get('opciones-metrica')
    labelsObj = request.form.get('opciones-labels')
    labels = json.loads(labelsObj)

    df, img_url = pm.get_report(metric, labels)

    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=pm.get_all_metrics())

@main.route('/')
def index():
    return render_template('index.html', tables=[], titles="", img_url="", valores=pm.get_all_metrics())
