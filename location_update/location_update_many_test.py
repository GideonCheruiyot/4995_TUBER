#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:44:00 2019

@author: red
"""

import pymongo
import dns
from bson.son import SON

client = pymongo.MongoClient("mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true")
db = client.users
cache = db.mentor_cache

bulk = cache.initialize_unordered_bulk_op()

new_locations = [[-74.0672519, 40.74764642], [-74.0672519, 40.74764641]]
id_s = [1, 2]

i = 0
for id in id_s:
    # process in bulk
    bulk.find({ '_id': id }).update({ '$set': { 'loc': new_locations[i] } })
    i += 1

bulk.execute()