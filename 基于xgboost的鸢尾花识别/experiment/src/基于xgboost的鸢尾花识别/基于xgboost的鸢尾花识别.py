
# coding: utf-8

# In[1]:


import pandas as pd
data_iris = pd.read_csv('/root/experiment/datas/iris.csv')
data_iris.shape


# In[2]:


data_iris.head(5)


# In[3]:


data_iris.describe()


# In[4]:


data_iris.isnull().sum()


# In[5]:


import matplotlib.pyplot as plt
data_iris.hist(figsize=(8,6))
plt.show()


# In[6]:


plt.figure(figsize=(8,6))
plt.scatter(x=data_iris['petal_l'], y=data_iris['petal_w'],c=data_iris['classes'])
plt.show()


# In[7]:


plt.figure(figsize=(8,6))
plt.scatter(x=data_iris['sepal_l'], y=data_iris['sepal_w'],c=data_iris['classes'])
plt.show()


# In[8]:


X = data_iris.iloc[:,:-1]
y = data_iris.iloc[:,-1]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)


# In[9]:


import xgboost as xgb
params = {
    'learning_rate':0.2,
    'n_estimators':2,
    'max_depth':2,
    'min_child_weight':1,
    'gamma':0,
    'subsample':0.8,
    'colsample_bytree':0.8,
    'silent':True,
    'objective':'multi:softmax',
}
model = xgb.XGBClassifier(**params)
from sklearn.model_selection import GridSearchCV
grid_params = {
        'min_child_weight':[x for x in range(2,6)]
}

grid = GridSearchCV(model,grid_params,cv=3)
grid.fit(X_train,y_train)


# In[10]:


grid.best_params_


# In[11]:


print("Accuracy:{0:.1f}%".format(100*grid.best_score_))


# In[12]:


params = {
    'learning_rate':0.2,
    'n_estimators':3,
    'max_depth':2,
    'min_child_weight':2,
    'gamma':0,
    'subsample':0.8,
    'colsample_bytree':0.8,
    'silent':True,
    'objective':'multi:softmax',
}
model = xgb.XGBClassifier(**params) 
model.fit(X_train, y_train,eval_set=[(X_train, y_train), (X_test, y_test)], eval_metric='merror')
model.evals_result()

