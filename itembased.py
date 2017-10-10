
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

class ItemBased():
    
    
    def __init__(self):
        path = '/home/admin-ygb/Desktop/recommender system/data/'
        columns = ['user_id', 'item_id', 'rating', 'timestamp']
        self.train = pd.read_csv(path + 'ua.base', sep='\t', names=columns)
        self.n_users = 943
        self.n_items = 1682
        self.train_matrix = np.zeros((self.n_users, self.n_items))
        self.whole_item = self.train.item_id.unique()
        for each in self.train.itertuples():
            #print(each)
            self.train_matrix[each.user_id-1, each.item_id-1] = each.rating
        self.item_similarity = pairwise_distances(self.train_matrix.T, metric='cosine')

    def construct_score_dict(self):
        """construct the data structrue the data like {'1': {'1': 5,'101': 2,'105': 2,'106': 4,....}    first '1' is the user 1,and the second dict include the all movie user1 has rated movie:score"""
        train_data_construct = self.train
        train_data_construct = train_data_construct.to_dict(orient='records')
        for i,value in enumerate(train_data_construct):
            value = {str(value['user_id']):{str(value['item_id']):value['rating']}}
            train_data_construct[i] = value
        dic = {}
        for each in train_data_construct:
            for key, value in each.items():
                dic.setdefault(key, []).append(value)
        for key, values in dic.items():
            m = {}
            for each in values:
                m.update(each)
            dic[key] = m 
        self.train = dic

    def itembased(self,predict_user):
        result = {}
        userRating = self.train[predict_user]
        for pre_item in self.whole_item:
            if str(pre_item) not in userRating:
                total_similarity = 0
                for exist_item in userRating:
                    total_similarity += self.item_similarity[pre_item-1][int(exist_item)-1]
                for exist_item in userRating:
                    if pre_item not in result:
                        result[pre_item] = self.item_similarity[pre_item-1][int(exist_item)-1] / total_similarity                        * userRating[exist_item]
                    else:
                        result[pre_item] = result[pre_item] + self.item_similarity[pre_item-1][int(exist_item)-1]                         / total_similarity * userRating[exist_item]
        result = list(result.items())
        result.sort(key=lambda x: x[1],reverse=True)
        return result
                
if __name__ == '__main__':
    itembased = ItemBased()
    itembased.construct_score_dict()