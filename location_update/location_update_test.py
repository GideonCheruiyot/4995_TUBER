#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:33:14 2019

@author: red
"""


import pymongo
import dns
from bson.son import SON

client = pymongo.MongoClient("mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true")
db = client.users
cache = db.mentor_cache

# important: longitude first
new_location = [-74.0672519, 40.74764641]
id_ = 1
# SORTED (yay) mentors nearest to the center in a given radius
find_mentor = {"_id": 1}

query = { "loc": new_location }
new_value = { "$set": query }

cache.update_one(find_mentor, new_value)
