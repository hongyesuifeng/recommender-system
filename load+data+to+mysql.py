
# coding: utf-8

# In[3]:

import pymysql as mysqldb  
import pandas as pd  
import pymysql.cursors  
import datetime   
from sqlalchemy import create_engine 


# In[4]:

columns = ['user_id', 'item_id', 'rating', 'timestamp']


# In[5]:

#train = pd.read_csv("/home/admin-ygb/Desktop/ml-10M100K/ra.train",sep='::',names=columns)


# In[6]:

test = pd.read_csv("/home/admin-ygb/Desktop/ml-10M100K/ra.test",sep='::',names=columns)


# In[8]:

#train.head()


# In[9]:

test.head()


# In[10]:

engine = create_engine("mysql+pymysql://root:admin@localhost/recommender?charset=utf8",echo=True) 


# In[7]:

#train.to_sql(name='train', con=engine, if_exists = 'append', index=False, chunksize=1000)

test.to_sql(name='test', con=engine, if_exists = 'append', index=False, chunksize=1000)
# In[8]:




# In[9]:




# In[10]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[11]:




# In[12]:




# In[13]:




# In[14]:




# In[15]:




# In[16]:




# In[17]:




# In[29]:




# In[ ]:




# In[43]:




# In[30]:

#print("test{}.txt".format(j))


# In[44]:




# In[42]:




# In[ ]:




# In[32]:




# In[21]:




# In[22]:




# In[20]:




# In[ ]:




# In[93]:




# In[70]:




# In[77]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



