import time
from flask import Flask

import vega_datasets
import altair as alt

app = Flask(__name__)

@app.route('/time')
def get_time():
    return {'time': time.time()}

@app.route('/vega')
def get_vega_js():
    cars = vega_datasets.data('cars')
    chart = alt.Chart(cars)
    chart = chart.mark_point().encode(x='Displacement')
    return chart.to_json()