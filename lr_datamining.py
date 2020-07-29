#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Data.PreProcessing import fetchData
from Data.PreProcessing import fetchLabels
from Algorithms.testingUtil import getScore
from Algorithms.testingUtil import plotTracing
import os
from sklearn.linear_model import LogisticRegression
import matplotlib as plt


# In[2]:


data = []

for fileName in os.listdir('Data/csvData'):
    if fileName.startswith('mar9'):
        f = 'Data/csvData/' + fileName
        data.append(fetchData(f))
        
print(data[4][1000])


# In[3]:


labels = [];

for point in data:
    labelset = fetchLabels(point, 2020, 3, 9, 48.4634, -123.3117, -8)
    labels.append(labelset)

print(labels[1][1000])


# In[24]:


LR_a = LogisticRegression(penalty='l2', C = 1.0, solver = 'lbfgs', max_iter = 100);
LR_b = LogisticRegression(penalty='l2', C = 1.0, solver = 'lbfgs', max_iter = 100);

train_set = [];
train_labels = [];

alphas = [];
betas = [];

for point in range(len(data)-1):
    for line in data[point]:
        alpha = line[4]
        beta = line[5]
                
        '''The angle of the device works such that when laying flat and aligned with it's marker, it is at (0, 0).
        In our case the marker pointed south. Here, we adjust it so that they corrospond to altitude and azimuth'''

        if(alpha < 90):
            alpha_alt = alpha
            beta_alt = beta + 90
        else:
            alpha_alt = 90 - abs(90 - alpha)
            beta_alt = (360 + (beta - 90))%360
    
        train_set.append([alpha_alt, beta_alt]);
        alphas.append(alpha_alt)
        betas.append(beta_alt)

l_alphas = [];
l_betas = [];       

for point in range(len(labels)-1):
    for line in labels[point]:
        train_labels.append(line) 
        l_alphas.append(line[0])
        l_betas.append(line[1]) 
        
l_alphas = [round(i) for i in l_alphas] 
l_betas = [round(i) for i in l_betas]

LR_a.fit(train_set, l_alphas)
LR_b.fit(train_set, l_betas);

predictions_a = LR_a.predict(train_set);
predictions_b = LR_b.predict(train_set);


# In[25]:


#The average number of degrees the angle is off by.
def getAvg(predict, labels):
    dif = 0;
    for point in range(len(predict)):
        dif += abs(predict[point]-labels[point])
    dif = dif/len(predict)
    return dif

a = getAvg(predictions_a, l_alphas);
b = getAvg(predictions_b, l_betas);

print([a, b])


# In[26]:


predictions = [];
temp_labels = [];
for x in range(len(predictions_a)):
    predictions.append([predictions_a[x], predictions_b[x]])
    temp_labels.append([l_alphas[x], l_betas[x]])

print('ALPHA')
templist = []
for x in range(len(predictions_a)):
    if(abs(predictions_a[x] - l_alphas[x]) > 5):
        if [predictions_a[x], l_alphas[x]] not in templist:
            print([predictions_a[x], l_alphas[x]])
            templist.append([predictions_a[x], l_alphas[x]])

print('BETA')
templist = []
for x in range(len(predictions_b)):
    if(abs(predictions_b[x] - l_betas[x]) > 5):
        if [predictions_b[x], l_betas[x]] not in templist:
            print([predictions_b[x], l_betas[x]])
            templist.append([predictions_b[x], l_betas[x]])
            
score = getScore(predictions, temp_labels, 30)
plotTracing(predictions, None, temp_labels)


# In[27]:


test_labels = [];
test_set = [];
t_alphas = [];
t_betas = [];       

point = len(data) - 1
for line in data[point]:
        alpha = line[4]
        beta = line[5]

        if(alpha < 90):
            alpha_alt = alpha
            beta_alt = beta + 90
        else:
            alpha_alt = 90 - abs(90 - alpha)
            beta_alt = (360 + (beta - 90))%360
    
        test_set.append([alpha_alt, beta_alt]);
        alphas.append(alpha_alt)
        betas.append(beta_alt)

for line in labels[point]:
    test_labels.append(line)
    t_alphas.append(line[0])
    t_betas.append(line[1]) 
        
t_alphas = [round(i) for i in t_alphas] 
t_betas = [round(i) for i in t_betas]

predictions_at = LR_a.predict(test_set);
predictions_bt = LR_b.predict(test_set);


# In[28]:


a = getAvg(predictions_at, t_alphas);
b = getAvg(predictions_bt, t_betas);

print([a, b])


# In[29]:


predictionst = [];
temp_labels = [];
for x in range(len(predictions_at)):
    predictionst.append([predictions_at[x], predictions_bt[x]])
    temp_labels.append([t_alphas[x], t_betas[x]])

print('ALPHA')
templist = []
for x in range(len(predictions_at)):
    if(abs(predictions_at[x] - t_alphas[x]) > 10):
        if [predictions_at[x], t_alphas[x]] not in templist:
            print([predictions_at[x], t_alphas[x]])
            templist.append([predictions_at[x], t_alphas[x]])

print('BETA')
templist = []
for x in range(len(predictions_bt)):
    if(abs(predictions_bt[x] - t_betas[x]) > 10):
        if [predictions_bt[x], t_betas[x]] not in templist:
            print([predictions_bt[x], t_betas[x]])
            templist.append([predictions_bt[x], t_betas[x]])

score = getScore(predictionst, temp_labels, 30)


# In[30]:


plotTracing(predictionst, None, temp_labels)


# In[16]:


the_set = [];
the_alphas = [];
the_betas = [];

for point in range(len(data)):
    for line in data[point]:
        alpha = line[4]
        beta = line[5]
        
        if(alpha < 90):
            alpha_alt = alpha
            beta_alt = beta + 90
        else:
            alpha_alt = 90 - abs(90 - alpha)
            beta_alt = (360 + (beta - 90))%360
    
        the_set.append([alpha_alt, beta_alt]);
        the_alphas.append(alpha_alt)
        the_betas.append(beta_alt)

the_labels = [];
labels_a = [];
labels_b = [];       

for point in range(len(labels)):
    for line in labels[point]: 
        labels_a.append(line[0])
        labels_b.append(line[1]) 
        
labels_a = [round(i) for i in labels_a]
labels_b = [round(i) for i in labels_b]

for x in range(len(the_set)):
    the_labels.append([labels_a[x], labels_b[x]])
    
score = getScore(the_set, the_labels, 100)

the_subset = []
the_sublabels = []
count = 164173
print(len(the_set))
while count < len(the_set):
    the_subset.append(the_set[count])
    the_sublabels.append(the_labels[count])
    count = count + 1
plotTracing(predictionst, the_subset, labels[point])


# In[38]:


x1 = predictions_at[400:]
y1 = predictions_bt[400:]

plt.pyplot.plot(y1, x1, linestyle='dashed')
plt.pyplot.plot(t_betas, t_alphas, linestyle='dashed')
plt.pyplot.plot(l_betas, l_alphas, linestyle='dashed')


# In[ ]:




