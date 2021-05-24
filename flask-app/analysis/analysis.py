import numpy as np
import pandas as pd
import datetime as dt
import sys

"""
    Analysis
"""
class DataAnalysis:
    def __init__(self, data_path='') -> None:
        self.dm = DataManager(data_path)
        self.data = self.dm.fetch()
        self.sales_nov, self.carts_nov, self.views_nov = None, None, None
        self.analyser = Analyser()

        self.data_preprocess()

    def data_preprocess(self):
        if not (self.sales_nov and self.carts_nov and self.views_nov):
            self.sales_nov, self.carts_nov, self.views_nov = self.analyser.pre_process(self.data)

    '''Supported analyses'''
    # TODO: exceptions
    def top_categories_by_num_sales(self, top=10):
        return self.analyser.generate_base_counts(
            self.sales_nov, metrics='product_id', grouped='category_code', top=top)

    def top_categories_by_revenues(self, top=10):
        return self.analyser.generate_base_sum(
            self.sales_nov, metrics='price', grouped='category_code', top=top)

    def nov_conversions(self):
        top_10_cat_sales = self.top_categories_by_num_sales()
        return self.analyser.conversions(
            self.data, grouped='category_code', metric='user_session', comp=top_10_cat_sales)
    
    def nov_funnel(self):
        return self.analyser.funnel(self.data, grouped='category_code', metric='user_session')


"""
    Data
"""
class DataManager:
    def __init__(self, data_path='') -> None:
        self.data_path = data_path
        self.data = None

    # Fetch data
    # TODO: 1. can be converted to database; 2. specify nrows
    def fetch(self):
        if not self.data:
            try:
                self.data = pd.read_csv(self.data_path, nrows=1000)
            except:  # TODO: more specific error handling
                print('Unexpected error:', sys.exc_info()[0])
        return self.data


"""
    Analyser
"""
class Analyser:
    def __init__(self) -> None:
        pass

    # TODO: need to be split later on
    def pre_process(self, nov):
        """
            Input: nov
            Return: sales_nov, carts_nov, views_nov
        """
        nov.event_time = pd.to_datetime(nov["event_time"]).dt.date

        sales_nov = nov.loc[nov.event_type == 'purchase']
        carts_nov = nov.loc[nov.event_type == 'cart']
        views_nov = nov.loc[nov.event_type == 'view']

        return sales_nov, carts_nov, views_nov

    '''Helpers'''
    def generate_base_counts(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).count().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).count().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]


    def generate_base_sum(self, data, metrics, grouped, top, asc=False, subset=(), choice=()):
        if subset != ():
            data_up = data.loc[data[subset] == choice]
            data_up = data_up.groupby([grouped]).sum().loc[:, [metrics]]
        else:
            data_up = data.groupby([grouped]).sum().loc[:, [metrics]]
        data_up.reset_index(inplace=True)
        data_up = data_up.sort_values(by=metrics, axis=0, ascending=asc)

        return data_up.iloc[:top+1, :]


    def conversions(self, data, grouped, metric, comp, subset=(), choice=()):
        if subset != ():
            nov_grouped = data.loc[data[subset] == choice]
            nov_grouped = nov_grouped.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]
        else:
            nov_grouped = data.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped = nov_grouped.pivot(
            index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped['v2c: views to cart'] = (nov_grouped.cart/nov_grouped.view)
        nov_grouped['c2p: cart to payment'] = (
            nov_grouped.purchase/nov_grouped.cart)
        nov_grouped['v2p: views to payment'] = (
            nov_grouped.purchase/nov_grouped.view)
        nov_grouped = nov_grouped.loc[nov_grouped[grouped].isin(
            list(comp[grouped].unique()))]
        nov_grouped_t = nov_grouped.T.loc[[
            grouped, 'v2c: views to cart', 'c2p: cart to payment', 'v2p: views to payment']]
        nov_grouped_t.columns = nov_grouped_t.loc[grouped, :]
        nov_grouped_t = nov_grouped_t.drop(grouped)
        nov_grouped_t.reset_index(inplace=True)
        nov_grouped_t = nov_grouped_t.melt(id_vars=['event_type'],
                                        var_name=grouped,
                                        value_name="conversion_value")
        return nov_grouped_t


    def funnel(self, data, grouped, metric, subset=(), choice=()):
        if subset != ():
            nov_grouped = data.loc[data[subset] == choice]
            nov_grouped = nov_grouped.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]
        else:
            nov_grouped = data.groupby(
                [grouped, 'event_type']).count().loc[:, [metric]]

        nov_grouped[grouped] = nov_grouped .index.get_level_values(0)
        nov_grouped['event_type'] = nov_grouped .index.get_level_values(1)
        nov_grouped = nov_grouped.pivot(
            index=grouped, columns='event_type', values=metric).reset_index()
        nov_grouped = nov_grouped.dropna().T
        nov_grouped.columns = nov_grouped.loc[grouped, :]
        nov_grouped = nov_grouped.drop(grouped)
        nov_grouped.reset_index(inplace=True)
        nov_grouped = nov_grouped.melt(id_vars=['event_type'],
                                    var_name=grouped,
                                    value_name="funnel_value")
        return nov_grouped


