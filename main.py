#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pymongo
import json
import requests
import os
from dotenv import load_dotenv


# In[33]:


load_dotenv()

API_KEY = os.getenv('KEY')
DB_CONNECTION = os.getenv('DB_string')


# In[42]:





# In[43]:



DB_NAME = "BetMe"

# Establish a connection with mongoDB
client = pymongo.MongoClient(DB_CONNECTION)

# Create a DB
dataBase = client[DB_NAME]


# In[47]:


client.list_database_names()


# In[45]:


def checkExistence_DB(DB_NAME, client):
    """It verifies the existence of DB"""
    DBlist = client.list_database_names()
    if DB_NAME in DBlist:
        print(f"DB: '{DB_NAME}' exists")
        return True
    print(f"DB: '{DB_NAME}' not yet present OR no collection is present in the DB")
    return False


_ = checkExistence_DB(DB_NAME=DB_NAME, client=client)


# In[48]:


COLLECTION_NAME = "All_Sports"
collection = dataBase[COLLECTION_NAME]


# In[49]:


# let's verify whether we have our database in the list or not 
# we'll use the following function:-

def checkExistence_COL(COLLECTION_NAME, DB_NAME, db):
    """It verifies the existence of collection name in a database"""
    collection_list = db.list_collection_names()
    
    if COLLECTION_NAME in collection_list:
        print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' exists")
        return True
    
    print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' does not exists OR \n    no documents are present in the collection")
    return False


_ = checkExistence_COL(COLLECTION_NAME=COLLECTION_NAME, DB_NAME=DB_NAME, db=dataBase)


# In[66]:


Sports = dataBase.create_collection("All_Sports")


# In[69]:


def create_all_sports_data():    
    try:
        request_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
        'api_key': API_KEY})
     
        sports_json = json.loads(request_response.text)
        Sports.insert_many(sports_json['data'])   
       
    except Exception as e:
        print(str(e))


create_all_sports_data()


# In[70]:





# In[ ]:


total_in_play = dataBase.create_collection("in-play_all_regions")


# In[74]:


regions = ["uk", "us", "eu", "au"]

def total_upcoming_sports():
    for region in regions:
        sport_key = 'upcoming'
        try:
            odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
                'api_key': API_KEY,
                'sport': sport_key,
                'region': regions, 
                'mkt': 'h2h', 
                'dateFormat': 'iso'})
            
            in_play_data = json.loads(odds_response.text)
            total_in_play.insert_many(in_play_data['data'])
            
        except Exception as e:
            print(str(e))
                

total_upcoming_sports()


# In[ ]:




