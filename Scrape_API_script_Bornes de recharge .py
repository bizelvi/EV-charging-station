#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install urlopen


# In[1]:


from urllib.request import urlopen
from pandas.io.json import json_normalize
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import requests
import json
import pandas as pd


# In[2]:


#Get the data from opendata JSON API

opdata_url='https://opendata.bruxelles.be/api/records/1.0/search/?dataset=bornes-de-recharge-pour-voitures-electriques&q=&rows=10000'

response = urlopen(opdata_url)# +"timeseries/#?expanded=true")
#response = requests.request("POST",opdata_url)#, headers=headers)
    
json_data=response.read().decode('utf-8','replace')
with open('opdata.json','w') as f:
    json.dump(json_data, f)
json.loads(json_data)


# In[3]:


opdata = json.loads(json_data)
opdata_df= pd.json_normalize(opdata,errors='raise', max_level=7)
opdata_df.head(10)


# In[4]:


opdata = json.loads(json_data)
opdata_df1 = pd.json_normalize(opdata['records'],errors='raise', max_level=7)
opdata_df1.head(10)


# In[5]:


opdata_df1.to_csv('opdata_loc.csv',sep=';',index=True)


# In[6]:


opdata_df1.to_csv('/Users/Elvis/Desktop/ULB/Thesis files /datasets/opdata.csv', index=False)


# In[13]:


#!pip install geopandas


# In[20]:


import geopandas as gpd
geo_pd = gpd.GeoDataFrame(opdata_df1, geometry=gpd.points_from_xy(opdata_df1['fields.wgs84_long'],opdata_df1['fields.wgs84_lat']))


# In[18]:


#import geopandas as gpd
geo_pd = gpd.GeoDataFrame(opdata_df1, geometry=gpd.points_from_xy(opdata_df1['fields.wgs84_long'], opdata_df1['fields.wgs84_lat']))                      


# In[21]:


geo_pd.head()


# In[22]:


geo_pd.columns 


# In[62]:


geo_pd.drop(axis=0, index=None, columns=['fields.typefr','fields.adrvoisnl','fields.typedut','fields.typeeng','fields.z_pcdd','fields.z_pcdd_fr','fields.z_pcdd_fr'],inplace=False)


# In[27]:


#!pip install shapely 
#!pip install Polygon


# In[26]:


import shapely
import polygon
import numpy as np
import pandas as pd
from pyproj import Proj, transform
import matplotlib.pyplot as plt


# In[29]:


# pyproj transform geometry data onto Lambert 1972 GIS coordinates 
outProj = Proj(init='epsg:4326')#références longitude latitude


# In[30]:


shp_file="/Users/Elvis/Desktop/ULB/Thesis files /shape_files/sh_statbel_statistical_sectors_31370_20220101.shp"

#lecture du shp en geodataframe. 
fichier_shp = gpd.read_file(shp_file)

# convertion du fichier lambert vers le référentiel latitude longitude :affectation du crs, puis conversion
fichier_shp_lambert = fichier_shp.set_crs("EPSG:31370", allow_override=True)
statistical_sector=fichier_shp_lambert.to_crs('epsg:4326') ##coordonnées en lat / long


# ## Note :)
# The statistical sector is the smallest entity used to collect individual data( such as the taxable income, number of househould)
# without without revealing the identity 

# In[45]:


statistical_sector.boundary.plot()


# In[32]:


statistical_sector.columns


# In[35]:


statistical_sector.shape


# In[36]:


statistical_sector.head()


# In[55]:


#select only brussels statistical sectors  As we got the charging position of brussels region
bxl=statistical_sector[statistical_sector['CNIS_REGIO']=='04000'].reset_index()
bxl.head()


# In[48]:


bxl.boundary.plot()
figsize=(15, 15)


# In[68]:


geo_pd.head()


# #Loop
# Create a loop tp commpare the the dataset for the charging 

# In[59]:


for i in range(opdata_df1.shape[0]):
    for j in range(bxl.shape[0]):
        result=bxl.loc[j,'geometry'].contains(opdata_df1.loc[i,'geometry'])
        if result==True:
            opdata_df1.loc[i,'datasetid']=bxl.loc[j,'CS01012022'] 
            print(result)
        


# In[69]:


for i in range(opdata_df1.shape[0]):
    for j in range(bxl.shape[0]):
        result=bxl.loc[j,'geometry'].contains(opdata_df1.loc[i,'geometry'])
        if result==True:
            opdata_df1.loc[i,'recordid']=bxl.loc[j,'CS01012022']
            print(result)
        


# In[65]:


#opdata_df1.head()
geo_pd.head()


# In[67]:


for i in range(geo_pd.shape[0]):
    for j in range(bxl.shape[0]):
        result=bxl.loc[j,'geometry'].contains(geo_pd.loc[i,'geometry'])
        if result==True:
            geo_pd.loc[i,'datasetid']=bxl.loc[j,'CS01012022'] 
            print(result)


# In[80]:


#col rename datasetid== CS01012022
opdata_df1.rename(columns={'datasetid':'CS01012022'}, inplace=True)


# In[82]:


opdata_df1.drop(columns=['recordid','fields.typefr','fields.wgs84_lalo','fields.adrvoisnl','fields.typedut','fields.typeeng','geometry.coordinates','fields.z_pcdd_nl','fields.z_pcdd_fr','fields.z_pcdd'])


# In[ ]:


# save opdata_df1 as cvs file


# # scrape new appi for belgian districts
#  /api/records/1.0/search/?dataset=belgium-statistical-districts%40public&q=&sort=inhab&facet=sector_fr&facet=commune&facet=arrond_fr&facet=prov_fr&facet=reg_fr
# 

# In[ ]:





# In[ ]:


#Get the data from opendata JSON API

opdata_url='https://data.opendatasoft.com/api/records/1.0/search/?dataset=belgium-statistical-districts%40public&q=&rows=100&sort=inhab&facet=sector_fr&facet=commune&facet=prov_fr&facet=reg_fr'
response = urlopen(opdata_url)

json_data=response.read().decode('utf-8','replace')
with open('opdata.json','w') as f:
    json.dump(json_data, f)
json.loads(json_data)


# In[ ]:


new_data = json.loads(json_data)
new_data_df = pd.json_normalize(new_data, max_level=7)
new_data_df.head(10)


# In[ ]:


new_data = json.loads(json_data)
new_data_df = pd.json_normalize(new_data['facet_groups'], max_level=7)
new_data_df.head(10)

