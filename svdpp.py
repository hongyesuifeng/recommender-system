
import numpy as np
import pandas as pd


class SVDPP():
    
    
    def __init__(self):
        """read train and test and Initialize parameters"""    
        
        path = '/home/admin-ygb/Desktop/recommender system/data/'
        columns = ['user_id', 'item_id', 'rating', 'timestamp']
        self.train = pd.read_csv(path + 'ua.base', sep='\t', names=columns)
        self.n_users = 943
        self.n_items = 1682
        self.whole_item = self.train.item_id.unique()
        
        self.mean = 0
        self.std_dev = 0.1
        self.n_factors = 15
        self.n_epochs = 5
        self.biased = True
        
        self.bu = np.zeros(self.n_users, np.double)
        self.bi = np.zeros(self.n_items, np.double)
        self.pu = np.random.normal(self.mean, self.std_dev,(self.n_users, self.n_factors))
        self.qi = np.random.normal(self.mean, self.std_dev,(self.n_items, self.n_factors))
        self.global_mean = self.train.rating.mean()
        self.yj = np.random.normal(self.mean, self.std_dev,(self.n_items, self.n_factors))
        self.impl_fdb = np.zeros(self.n_factors, np.double)   
        
        self.Gamma = 0.005
        self.Lambda1 = 0.02
        self.Lambda2 = 0.015
        self.trainset = 0
        self.construct_score_dict()

    def svdpp(self):
        for current_epoch in range(self.n_epochs):
            print("this is the step:", current_epoch)
            for each in self.train.itertuples():
                print("now is the index: ",each.Index)
                u = each.user_id - 1
                i = each.item_id - 1
                r = each.rating
                sqrt_u = np.sqrt(len(self.trainset[str(u+1)]))
                self.impl_fdb = np.zeros(self.n_factors, np.double)
                for j in self.trainset[str(u+1)].keys():
                    for f in range(self.n_factors):
                        self.impl_fdb[f] += self.yj[int(j)-1,f] / sqrt_u

                # compute current error
                dot = 0  # <q_i, p_u>
                for f in range(self.n_factors):
                    dot += self.qi[i, f] * (self.pu[u, f] + self.impl_fdb[f])
                err = r - (self.global_mean + self.bu[u] + 
                           self.bi[i] + dot)
        
                # update biases
                if self.biased:
                    self.bu[u] += self.Gamma * (err - self.Lambda1 * self.bu[u])
                    self.bi[i] += self.Gamma * (err - self.Lambda1 * self.bi[i])
        
                # update factors
                for f in range(self.n_factors):
                    puf = self.pu[u, f]
                    qif = self.qi[i, f]
                    self.pu[u, f] += self.Gamma * (err * qif - self.Lambda2 * puf)
                    self.qi[i, f] += self.Gamma * (err * (puf + self.impl_fdb[f]) - self.Lambda2 * qif)
                    for i in self.trainset[str(u+1)].keys():
                        self.yj[int(j)-1,f] += self.Gamma * (err * qif / sqrt_u - self.Lambda2 * self.yj[int(j)-1,f])
                        
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
        self.trainset = dic

    def predict(self,predict_user):
        """this is the predict function,predict_user is the 
           user you want to predict"""
        result = {}
        userRating = self.train[predict_user]
        for pre_item in self.whole_item:
            if str(pre_item) not in userRating:
                result[str(pre_item)] = self.global_mean + \
                      + self.bu[int(predict_user)-1] + self.bi[int(pre_item)-1] +\
                           np.dot(self.qi[int(pre_item)-1],self.pu[int(predict_user)-1])
        result = list(result.items())
        result.sort(key=lambda x: x[1],reverse=True)
        return result

    def predict_top10(self,predict_user):
        """this is the predict function,predict_user is the 
           user you want to predict"""
        result = {}
        userRating = self.train[predict_user]
        for pre_item in self.whole_item:
            if str(pre_item) not in userRating:
                result[str(pre_item)] = self.global_mean + \
                      + self.bu[int(predict_user)-1] + self.bi[int(pre_item)-1] +\
                           np.dot(self.qi[int(pre_item)-1],self.pu[int(predict_user)-1])
        result = list(result.items())
        result.sort(key=lambda x: x[1],reverse=True)
        return result[:10]

        
        
if __name__ == '__main__':
    svdpp = SVDPP()
    svdpp.svdpp()
    

