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

'''Basic analysis/ visualization'''
# By category
# TODO: top x
@app.route('/top-categories-by-sales-with-revenue')
def get_top_categories_by_sales_with_revenue():
    top_cat_sales = data_analysis.top_categories_by_sales()
    chart_sales = alt.Chart(top_cat_sales, title='Top 10 categories by # of Sales').mark_bar().encode(
        x=alt.X('product_id:Q', title='# of sales'),
        y=alt.Y('category_code:N', sort='-x'),
    )

    top_ten_cat_by_revenues = data_analysis.top_categories_by_revenues()
    chart_revenues = alt.Chart(top_ten_cat_by_revenues, title='Total Revenue').mark_text().encode(
        y=alt.Y('category_code:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)

    chart = chart_sales | chart_revenues
    return chart.to_json()


@app.route('/top-categories-by-revenues')
def get_top_categories_by_revenues():
    top_ten_cat_by_revenues = data_analysis.top_categories_by_revenues()
    chart = alt.Chart(top_ten_cat_by_revenues, title='Total Revenue').mark_text().encode(
        y=alt.Y('category_code:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)
    return chart.to_json()

# TODO: top x
@app.route('/conversions')
def get_conversions():
    nov_funnel = data_analysis.funnel_by_category()
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


@app.route('/top-brands-by-sales-grouped-by-category')
def get_top_brands_by_sales_grouped_category():
    return {}


# By brand
@app.route('/top-brands-by-sales-with-revenues')
def get_top_brands_by_sales():
    chart1 = alt.Chart(data_analysis.top_brands_by_sales(), title='Top 10 brands by # of Sales').mark_bar().encode(
        x=alt.X('product_id:Q', title='# of sales'),
        y=alt.Y('brand:N', sort='-x'),
    )

    chart2 = alt.Chart(data_analysis.top_brands_by_revenues(), title='Total Revenue').mark_text().encode(
        y=alt.Y('brand:N', axis=None, sort='-text'),
        text='price:Q'
    ).properties(width=100)

    chart = chart1 | chart2
    return chart.to_json()


@app.route('/top-brands-by-conversions')
def get_top_brands_by_conversions():
    nov_funnel_by_brand = data_analysis.funnel_by_brand()

    brands = list(nov_funnel_by_brand.brand.unique())
    brand_dropdown = alt.binding_select(options=brands)
    brand_select = alt.selection_single(
        fields=['brand'], bind=brand_dropdown, name="Brand")

    chart = alt.Chart(nov_funnel_by_brand, title='Novemeber:Conversion for top 10 brands').mark_bar().encode(
        x=alt.X('event_type:N', sort=('view', 'cart', 'purchase')),
        y=alt.Y('funnel_value:Q'),
        column='brand:O'
    ).properties(
        width=200,
        height=300
    ).resolve_scale(y='independent').add_selection(
        brand_select
    ).transform_filter(
        brand_select
    ).properties(title="Select a Brand to Highlight It")
    return chart.to_json()


'''Recommendation'''
@app.route('/nearest-items')
def get_nearest_items():
    df = data_analysis.find_nearest_item(1003461)
    return df.to_html()