from .data_manager import *
from .recommender import *
from .analyser import *

"""
    DataAnalysis:
    1. Get data using DataManager
    2. Analyze data using Analyzer
    3. Make recommendation using Recommender
"""


class DataAnalysis:
    def __init__(self, data_path='') -> None:
        self.dm = DataManager(data_path)
        self.data = self.dm.fetch()

        # Data for basic analysis
        self.sales_nov, self.carts_nov, self.views_nov = None, None, None
        self.analyser = Analyser()
        self.data_preprocess_for_analysis()

        # Data for recommendation
        # Unique user and item
        self.unique_user, self.unique_item = set(), set()
        self.user_to_item, self.item_to_user = defaultdict(set), defaultdict(set)
        self.user_to_idx, self.itemid_to_category_code, self.itemid_to_brand = dict(), dict(), dict()
        self.recommender = Recommender()
        self.data_preprocess_for_recommendation()

    def data_preprocess_for_analysis(self):
        if not (self.sales_nov and self.carts_nov and self.views_nov):
            self.sales_nov = self.data.loc[self.data.event_type == 'purchase']
            self.carts_nov = self.data.loc[self.data.event_type == 'cart']
            self.views_nov = self.data.loc[self.data.event_type == 'view']

    def data_preprocess_for_recommendation(self):
        # Loop through all the rows and create a unique user and item set
        idx = 0
        for _, row in self.data.iterrows():
            userid, itemid, categorycode, brand = row[8], row[3], row[5], row[6] # TODO: wrongly indexed
            self.unique_user.add(userid)
            self.unique_item.add(itemid)

            if userid not in self.user_to_idx:
                self.user_to_idx[userid] = idx
                idx += 1

            self.user_to_item[userid].add(itemid)
            self.item_to_user[itemid].add(userid)
            self.itemid_to_category_code[itemid] = categorycode
            self.itemid_to_brand[itemid] = brand


    '''Supported analyses'''
    # TODO: exceptions
    # By category

    def top_categories_by_sales(self, top=10):
        return self.analyser.generate_base_counts(
            self.sales_nov, metrics='product_id', grouped='category_code', top=top)

    def top_categories_by_revenues(self, top=10):
        return self.analyser.generate_base_sum(
            self.sales_nov, metrics='price', grouped='category_code', top=top)

    def conversions_by_category(self):
        top_10_cat_sales = self.top_categories_by_sales()
        return self.analyser.conversions(
            self.data, grouped='category_code', metric='user_session', comp=top_10_cat_sales)

    def funnel_by_category(self):
        return self.analyser.funnel(self.data, grouped='category_code', metric='user_session')

    # By brand
    def top_brands_by_sales(self, top=10):
        return self.analyser.generate_base_counts(self.sales_nov, metrics='product_id', grouped='brand', top=top)

    def top_brands_by_revenues(self, top=10):
        return self.analyser.generate_base_sum(self.sales_nov, metrics='price', grouped='brand', top=10)

    def funnel_by_brand(self):
        return self.analyser.funnel(self.data, grouped='brand', metric='user_session')


    '''Supported recommendations'''
    def find_nearest_item(self, item=None):
        if not item:
            return
        
        nearest_items = self.recommender.find_nearest_item(item, self.item_to_user, self.user_to_item)
        items_df = pd.DataFrame([{
            'item_id': item_id,
            'category': self.itemid_to_category_code[item_id],
            'brand': self.itemid_to_brand[item_id]
        } for _, item_id in nearest_items]).transpose()

        return items_df