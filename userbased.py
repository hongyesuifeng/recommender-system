
# coding: utf-8

# In[16]:

import pandas as pd
from math import sqrt

class UserBased():
# In[3]:

    def __init__(self):
        
        path = '/home/admin-ygb/Desktop/recommender-system/data/'
        columns = ['user_id', 'item_id', 'rating', 'timestamp']
        self.train = pd.read_csv(path + 'ua.base', sep='\t', names=columns)
        #self.test = pd.read_csv('/home/admin-ygb/Desktop/recommender system/data/ua.test',sep='\t',names=names)
        
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

    def pearson(self, rating1, rating2):
        """calculate the user similarity in pearson"""
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def compute_nearest_neighbor(self, username, k=100):
        """compute the username's k nearest neighbors"""
        distances = []
        for instance in self.train:
            if instance != username:
                distance = self.pearson(self.train[username],self.train[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        return distances[0:k]

    def predict(self,predict_user,k):
        """userbased algorithm predict_user is the user you want
           to predict, k is the number of the user neighbors"""
        result = {}
        neighbors = self.compute_nearest_neighbor(predict_user,k)
        #print(neighbors)
        userRating = self.train[predict_user]
        total_similarity = 0
        total_score = 0
        for key in self.train[predict_user].keys():
            total_score += self.train[predict_user][key]
        average_score = total_score / len(self.train[predict_user])
        for i in range(k):
            total_similarity += abs(neighbors[i][1])
        for i in range(k):
            weight = neighbors[i][1] / total_similarity
            name = neighbors[i][0]
            neighborsRatings = self.train[name]
            #print("this is the neighborsRatings:", neighborsRatings)
            neighborsRatings_total_score = 0
            for key in neighborsRatings.keys():
                neighborsRatings_total_score += neighborsRatings[key]
            neighborsRatings_average_score = neighborsRatings_total_score / len(neighborsRatings)
            #print("this is neighbor_average:", neighborsRatings_average_score)
            #print("this is the neighbors: ",name)
            for each in neighborsRatings:
                #print("this is the item in every neighbors: ",each)
                if each not in userRating:
                    #print("gogo")
                    if each not in result:
                        result[each] = (neighborsRatings[each]- neighborsRatings_average_score)* weight
                    else:
                        result[each] = result[each] + (neighborsRatings[each] - neighborsRatings_average_score) * weight
        result = list(result.items())
        result.sort(key=lambda x: x[1],reverse=True)
        result = [(each[0],each[1]+average_score) for each in result]
        return result

    def predict_top10(self,predict_user,k):
        """userbased algorithm predict_user is the user you want
           to predict, k is the number of the user neighbors"""
        result = {}
        neighbors = self.compute_nearest_neighbor(predict_user,k)
        #print(neighbors)
        userRating = self.train[predict_user]
        total_similarity = 0
        total_score = 0
        for key in self.train[predict_user].keys():
            total_score += self.train[predict_user][key]
        average_score = total_score / len(self.train[predict_user])
        for i in range(k):
            total_similarity += abs(neighbors[i][1])
        for i in range(k):
            weight = neighbors[i][1] / total_similarity
            name = neighbors[i][0]
            neighborsRatings = self.train[name]
            #print("this is the neighborsRatings:", neighborsRatings)
            neighborsRatings_total_score = 0
            for key in neighborsRatings.keys():
                neighborsRatings_total_score += neighborsRatings[key]
            neighborsRatings_average_score = neighborsRatings_total_score / len(neighborsRatings)
            #print("this is neighbor_average:", neighborsRatings_average_score)
            #print("this is the neighbors: ",name)
            for each in neighborsRatings:
                #print("this is the item in every neighbors: ",each)
                if each not in userRating:
                    #print("gogo")
                    if each not in result:
                        result[each] = (neighborsRatings[each]- neighborsRatings_average_score)* weight
                    else:
                        result[each] = result[each] + (neighborsRatings[each] - neighborsRatings_average_score) * weight
        result = list(result.items())
        result.sort(key=lambda x: x[1],reverse=True)
        result = [(each[0],each[1]+average_score) for each in result]
        return result[:10]

                
    
if __name__ == '__main__':
    userbased = UserBased()
    userbased.construct_score_dict()
    
    

