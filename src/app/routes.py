from flask import Blueprint, render_template, request, jsonify
import json
from . import promMetrics
import warnings
warnings.filterwarnings("ignore")


main = Blueprint('main', __name__)
pm = promMetrics.PrometheusMetrics()

@main.route('/getReport', methods=['GET'])
def getReport():
    
    df, img_url = pm.get_report()
    
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=pm.get_all_metrics())

@main.route('/getReport', methods=['POST'])
def generateReport():
    
    metric = request.form.get('opciones-metrica')
    labels = json.loads(request.form.get('opciones-labels'))
    df, img_url = pm.generate_report(metric, labels)
    
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, img_url=img_url, valores=pm.get_all_metrics())

@main.route('/loadLabels', methods=['POST'])
def loadLabels():

    selected_value = request.form.get('selected_value')
    labels = pm.get_labels(selected_value)
    
    return jsonify(labels)

@main.route('/')
def index():
    return render_template('index.html', tables=[], titles="", img_url="", valores=pm.get_all_metrics())
