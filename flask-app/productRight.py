import time
from flask import Flask

import vega_datasets
import altair as alt

from .analysis import *

app = Flask(__name__)

# Initialize DataAnalysis class
mock_nov_data = '../mock-data/2019-Nov.csv'
data_analysis = DataAnalysis(data_path=mock_nov_data)


@app.route('/time')
def get_time():
    return {'time': time.time()}


@app.route('/vega')
def get_vega_js():
    cars = vega_datasets.data('cars')
    chart = alt.Chart(cars)
    chart = chart.mark_point().encode(x='Displacement')
    return chart.to_json()


@app.route('/top-categories-by-sales')
def get_top_categories_by_sales():
    top_ten_cat_sales = data_analysis.top_categories_by_num_sales()
    chart = alt.Chart(top_ten_cat_sales, title='Top 10 categories by # of Sales').mark_bar().encode(
        x=alt.X('product_id:Q', title='# of sales'),
        y=alt.Y('category_code:N', sort='-x'),
    )
    return chart.to_json()


@app.route('/top-categories-by-revenues')
def get_top_categories_by_revenues():
    top_ten_cat_by_revenues = data_analysis.top_categories_by_revenues()
    chart = alt.Chart(top_ten_cat_by_revenues, title='Total Revenue').mark_text().encode(
        y=alt.Y('category_code:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)
    return chart.to_json()

@app.route('/conversions')
def get_conversions():
    nov_funnel = data_analysis.nov_funnel()
    categories = list(nov_funnel.category_code.unique())

    cat_dropdown = alt.binding_select(options=categories)
    cat_select = alt.selection_single(
        fields=['category_code'], bind=cat_dropdown, name="Category")

    chart = alt.Chart(nov_funnel, title='Novemeber:Conversion for top 10 category_codes').mark_bar().encode(
        x=alt.X('event_type:N', sort=('view', 'cart', 'purchase')),
        y=alt.Y('funnel_value:Q'),
        column='category_code:O'
    ).properties(
        width=200,
        height=300
    ).resolve_scale(y='independent').add_selection(
        cat_select
    ).transform_filter(
        cat_select
    ).properties(title="Select a Category to Highlight It")
    return chart.to_json()