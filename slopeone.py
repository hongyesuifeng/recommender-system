import pandas as pd

class SlopeOne():
    """this is the slope one algorithm"""
    

    def __init__(self):
        """read train and test"""    
        
        path = '/home/admin-ygb/Desktop/recommender system/data/'
        columns = ['user_id', 'item_id', 'rating', 'timestamp']
        self.train = pd.read_csv(path + 'ua.base', sep='\t', names=columns)
        self.test = pd.read_csv(path + 'ua.test', sep='\t', names=columns)
        self.frequencies = {}
        self.deviations = {}
        
    def construct_score_dict(self):
        """construct the data structrue the data like {'1': {'1': 5,'101': 2,'105': 2,'106': 4,....}\
        first '1' is the user 1,and the second dict include the all movie user1 has rated movie:score"""
        
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


    def computeDeviations(self):
        """compute the deviation term of train data"""
        

        for ratings in self.train.values():
            # for each item & rating in that set of ratings:          
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})   
            # for each item2 & rating2 in that set of ratings:
                for (item2, rating2) in ratings.items():
                    if item != item2:
                        # add the difference between the ratings to our
                        # computation
    
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0.0)
    
                        self.deviations[item][item2] += (rating - rating2)
                        self.frequencies[item][item2] += 1
    
        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]
            
    
    #data = get_k_neighbor ,userRatings is the values  ,n is the number of the user , k is the number of the neighbours 
    def slopeOneRecommendations(self, predict_user):
        """the main process of slope one algorithm"""
        
        recommendations = {}
        frequencies = {}
        # for every item and rating in the user's recommendations
        for (userItem, userRating) in self.train[predict_user].items(): 
            # for every item in our dataset that the user didn't rate
            for (diffItem, diffRatings) in self.deviations.items():
                if diffItem not in self.train[predict_user] and \
                    userItem in self.deviations[diffItem]:
    
                    freq = self.frequencies[diffItem][userItem]
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # add to the running sum representing the numerator
                    # of the formula
                    recommendations[diffItem] += (diffRatings[userItem] +
                                             userRating) * freq
                    # keep a running sum of the frequency of diffitem
                    frequencies[diffItem] += freq
        #recommendations =  [(self.convertProductID2name(k),v / frequencies[k])for (k, v) in recommendations.items()]
        recommendations =  [(k,v / frequencies[k])for (k, v) in recommendations.items()]
        # finally sort and return
        recommendations.sort(key=lambda artistTuple: artistTuple[1],reverse = True)
        # I am only going to return the first 50 recommendations
        return recommendations
    
if __name__ == '__main__':
    slopeone = SlopeOne()
    slopeone.construct_score_dict()
    slopeone.computeDeviations()