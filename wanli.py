
# coding: utf-8

# In[8]:


import pandas as pd
import time
import numpy as np


# In[9]:


skip_prd_cols=[u'差级',u'厚度1',u'角度',u'密度',u'平方米重',u'平方米重1',u'后连续称',u'前连续称',               u'前测宽A',u'宽度（外层）',u'宽度3',u'面积3',u'面积4']


# In[10]:


produce_data = pd.read_csv('复合压出生产数据.csv',encoding='GBK')


# In[169]:


produce_data.shape


# In[11]:


produce_data.drop(skip_prd_cols,axis=1,inplace=True)


# In[12]:


jiance_data = pd.read_csv('复合压出轮廓检测数据.csv',encoding='GBK')


# In[175]:


produce_data.head()


# In[48]:


jiance_data.head()


# In[13]:


produce_data[u'采集时间_NUM']=produce_data[u'采集时间'].apply(lambda x:time.mktime(pd.Timestamp(x).timetuple()))
produce_data[u'检测时间_NUM'] =produce_data[u'采集时间_NUM']+160.0/produce_data[u'线速度']


# In[14]:


produce_data.sort_values(u'检测时间_NUM', inplace=True)
duplicate_bool = produce_data.duplicated(subset=[u'检测时间_NUM'], keep=False)
produce_data = produce_data.loc[duplicate_bool != True]
produce_data.reset_index(inplace=True,drop=True)


# In[15]:


jiance_data[u'检测时间_NUM']=jiance_data[u'检测时间'].apply(lambda x:time.mktime(pd.Timestamp(x).timetuple()))
jiance_data.sort_values(u'检测时间_NUM', inplace=True)
jiance_data.reset_index(inplace=True,drop=True)


# In[10]:


len(produce_data[u'检测时间'].unique())


# In[17]:


jiance_groups = jiance_data.groupby(u'检测时间_NUM')


# In[6]:


len(jiance_groups)


# In[44]:


result = []
count=0
for key,item in jiance_groups:
    #print key#,item
    if count%2000==0:
        print count
    count+=1
    tmp = key-produce_data[u'检测时间_NUM']
    tmp = tmp[tmp>=0].sort_values()
#     print tmp.iloc[0]
    if tmp.iloc[0]<=600:
        array = np.array(item)
        for a in array:
            result.append(np.concatenate([a, np.array(produce_data.ix[tmp.index[0]])]))
        
#     produce_data.ix[tmp.index[0]]
#     break


# In[52]:


col1=[]
for key,item in jiance_groups:
    col1 = item.columns
    break


# In[59]:


cols=list(col1)+(list(produce_data.columns))


# In[61]:


final_result = pd.DataFrame(result,columns=cols)


# In[62]:


final_result.shape


# In[63]:


final_result.to_csv('轮胎_clean.csv',index=False,encoding='utf8')


# In[25]:


# pd.options.display.float_format = '${:,.5f}'.format
# _input = 1526346869.1034484
#left = pd.DataFrame(result[0][1]).transpose()
# jiance_data.ix[(jiance_data[u'检测时间_NUM']-_input).argsort()[:2]]


# In[ ]:


# duplicate_bool1 = produce_data.duplicated(subset=[u'检测时间_NUM'], keep=False)


# produce_data.loc[duplicate_bool1 == True][[u'采集时间',u'线速度',u'产品编号', u'中机速度', u'操作工', u'计划产量', u'产线', u'配方', u'配方版本']].tail(100)

# produce_data.loc[duplicate_bool == True][u'检测时间_NUM'].head(10)
#produce_data.loc[duplicate_bool == True][[u'采集时间',u'采集时间_NUM',u'线速度',u'检测时间_NUM']].shape



# In[ ]:


# result=[]
# j,k=0,0
# len_jiance=jiance_data.shape[0]
# for i in range(32000,produce_data.shape[0]):#produce_data.shape[0]):
#     if i%20000==0:
#         print i
#     i_data = produce_data.iloc[i]
#     for k in range(j,len_jiance):
#         j_data = jiance_data.iloc[k]
#         if (j_data[u'检测时间_NUM']<i_data[u'采集时间_NUM']):
#             continue
#         if (j_data[u'检测时间_NUM']-i_data[u'采集时间_NUM'])<=600 and (j_data[u'检测时间_NUM']>=i_data[u'检测时间_NUM']):
#             print i_data[u'检测时间_NUM'],j_data[u'检测时间_NUM']
# #             break
# #             if jiance_data.iloc[k][u'检测时间_NUM']!=j_data[u'检测时间_NUM']:
# #                 j=k
# #             else:
# #                 result.append(np.concatenate((np.array(i_data), np.array(jiance_data.iloc[k])), axis=0))
#             tmp = j_data[u'检测时间_NUM']
#             while jiance_data.iloc[k][u'检测时间_NUM']==tmp:
#                 result.append(np.concatenate((np.array(i_data), np.array(jiance_data.iloc[k])), axis=0))
#                 k+=1
#             j=k
#             break
#         else:
#             break


