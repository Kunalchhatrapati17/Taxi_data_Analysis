#!/usr/bin/env python
# coding: utf-8

# In[1]:


import io
import pandas as pd
import requests


# In[19]:


df=pd. read_csv("Driver's_data.csv")


# In[20]:


df.head()


# In[21]:


df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])


# In[22]:


df = df.drop_duplicates().reset_index(drop=True)
df['trip_id'] = df.index


# In[23]:


df.head()


# In[24]:


datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].reset_index(drop=True)
datetime_dim['tpep_pickup_datetime'] = datetime_dim['tpep_pickup_datetime']
datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday

datetime_dim['tpep_dropoff_datetime'] = datetime_dim['tpep_dropoff_datetime']
datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday


datetime_dim['datetime_id'] = datetime_dim.index

# datetime_dim = datetime_dim.rename(columns={'tpep_pickup_datetime': 'datetime_id'}).reset_index(drop=True)
datetime_dim = datetime_dim[['datetime_id', 'tpep_pickup_datetime', 'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday',
                             'tpep_dropoff_datetime', 'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday']]
#
datetime_dim.head()


# In[25]:


passenger_count_dim = df[['passenger_count']].reset_index(drop=True)
passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
passenger_count_dim = passenger_count_dim[['passenger_count_id','passenger_count']]

trip_distance_dim = df[['trip_distance']].reset_index(drop=True)
trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
trip_distance_dim = trip_distance_dim[['trip_distance_id','trip_distance']]


# In[ ]:





# In[26]:


rate_code_type = {
    1:"Standard rate",
    2:"JFK",
    3:"Newark",
    4:"Nassau or Westchester",
    5:"Negotiated fare",
    6:"Group ride"
}
df['rate_code_name']=df['RatecodeID'].map(rate_code_type)

#rate_code_dim
rate_code_dim = df[['RatecodeID']].reset_index(drop=True)
rate_code_dim['rate_code_id'] = rate_code_dim.index
rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)
rate_code_dim = rate_code_dim[['rate_code_id','rate_code_name', 'RatecodeID']].drop_duplicates(subset=['RatecodeID'])

# rate_code_dim.head()


# In[27]:


rate_code_dim.head()


# In[28]:


pickup_location_dim = df[['pickup_longitude', 'pickup_latitude']].reset_index(drop=True)
pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
pickup_location_dim = pickup_location_dim[['pickup_location_id','pickup_latitude','pickup_longitude']] 


dropoff_location_dim = df[['dropoff_longitude', 'dropoff_latitude']].reset_index(drop=True)
dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
dropoff_location_dim = dropoff_location_dim[['dropoff_location_id','dropoff_latitude','dropoff_longitude']]


# In[29]:


payment_type_name = {
    1:"Credit card",
    2:"Cash",
    3:"No charge",
    4:"Dispute",
    5:"Unknown",
    6:"Voided trip"
}
df['payment_type_name']=df['payment_type'].map(payment_type_name)

payment_type_dim = df[['payment_type']].reset_index(drop=True)
payment_type_dim['payment_type_id'] = payment_type_dim.index
payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
payment_type_dim = payment_type_dim[['payment_type_id','payment_type','payment_type_name']].drop_duplicates(subset=['payment_type'])


# In[30]:


pip install openpyxl


# In[31]:


fact_table = df.merge(passenger_count_dim, left_on='trip_id', right_on='passenger_count_id', how='left') \
             .merge(trip_distance_dim, left_on='trip_id', right_on='trip_distance_id', how='left') \
             .merge(rate_code_dim, left_on='rate_code_name', right_on='rate_code_name', how='left') \
             .merge(pickup_location_dim, left_on='trip_id', right_on='pickup_location_id', how='left') \
             .merge(dropoff_location_dim, left_on='trip_id', right_on='dropoff_location_id', how='left')\
             .merge(datetime_dim, left_on='trip_id', right_on='datetime_id', how='left') \
             .merge(payment_type_dim, left_on='payment_type', right_on='payment_type', how='left') 

#Transferring data from fact_table to excel

output_file_name='Taxi_data.xlsx';

sheet_name='Fact Data'

fact_table.to_excel(output_file_name, sheet_name=sheet_name, index=False)

print(f"Data successfully to{output_file_name} on sheet '{sheet_name}'.")


# In[33]:


payment_type_dim.columns


# In[34]:


fact_table.columns


# In[35]:


fact_table


# In[32]:


#Transferring data from fact_table to excel

output_file_name='Uber_taxi_data.xlsx';

sheet_name='Fact Data'


fact_table(output_file_name, sheet_name=sheet_name, index=False)


print(f"Data successfully to{Output_file_name} on sheet '{sheet_name}'.")


# In[ ]:





# In[ ]:




