#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:53:32 2019

@author: red
"""

import pymongo
import dns
from bson.son import SON

client = pymongo.MongoClient("mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true")
db = client.users
cache = db.mentor_cache

# radius: ~1 mile = .017 units
# e.g. here within ~4 miles
radius = .07
# important: longitude first
student_location = [-74.0672518, 40.74764641]
# SORTED (yay) mentors nearest to the center in a given radius
query = {"loc": SON([("$near", student_location), ("$maxDistance", radius)])}

prelim = cache.find(query).limit(10)

results= []
for res in prelim:
    print(res)
    results.append(res)

# output is a list of dictionaries