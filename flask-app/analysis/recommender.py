import numpy as np
import pandas as pd
from collections import defaultdict
from numpy import dot
from numpy.linalg import norm

"""
    Recommender: make recommendation based on the input pandas.DataFrame
"""


class Recommender:
    def __init__(self) -> None:
        pass

    '''Recommendation Methods'''
    def find_nearest_item(self, itemid, item_to_user, user_to_item, top=10):
        maxSimilarityScore = float('-inf')
        ClosestItem = None
        candidateItems = set()
        users = item_to_user[itemid]
        similarities = []

        # reduce the search space of the candidate items
        for u in users:
            candidateItems = candidateItems.union(user_to_item[u])

        for item in candidateItems:
            if item==itemid:
                continue
            
            # score = CalcScore_cosine(item,itemid)
            score = self.jaccard(users, item_to_user[item])
            if score==float('nan'):
                continue

            similarities.append((score, item))
        similarities.sort(reverse=True)
        
        return similarities[:top]

    '''Helper'''
    def one_hot_encode(self, item, unique_user, item_to_user, user_to_idx):
        vector = [0 for _ in range(len(unique_user))]

        for user in item_to_user[item]:
            vector[user_to_idx[user]]=1
        
        return vector

    def CalcScore_cosine(self, item1, item2, unique_user, item_to_user, user_to_idx):
        a,b = self.one_hot_encode(item1, unique_user, item_to_user, user_to_idx), self.one_hot_encode(item2, unique_user, item_to_user, user_to_idx)

        cos_sim = dot(a, b)/(norm(a)*norm(b))
        return cos_sim

    def jaccard(self, s1, s2):
        numer = len(s1.intersection(s2))
        denom = len(s1.union(s2))
        return numer/denom