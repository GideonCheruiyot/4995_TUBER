#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:56:48 2019

@author: red
"""

import pymongo
import dns

co_url = "mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true"
client = pymongo.MongoClient(co_url)
db = client.users
user_info = db.user_info
mentor_cache = db.mentor_cache

sample_info = [{"_id": 1,
                "name": "Eddie",
                "phone": "(636) 403-3645"},
               {"_id": 2,
                "name": "Finbar",
                "phone": "(511) 798-7872"},
               {"_id": 3,
                "name": "Cassius",
                "phone": "(598) 811-0301"},
               {"_id": 4,
                "name": "Fahmida",
                "phone": "(204) 460-4466"},
               {"_id": 5,
                "name": "Maud",
                "phone": "(250) 828-4040"},
               {"_id": 6,
                "name": "Rebekka",
                "phone": "(422) 567-7496"},
               {"_id": 7,
                "name": "Armaan",
                "phone": "(215) 919-7472"},
               {"_id": 8,
                "name": "Vivek",
                "phone": "(642) 741-5072"},
               {"_id": 9,
                "name": "Donna",
                "phone": "((448) 622-9390"},
               {"_id": 10,
                "name": "Lilly-Mai",
                "phone": "(383) 337-9449"},
               {"_id": 11,
                "name": "Maddox",
                "phone": "(930) 882-4251"},
               {"_id": 12,
                "name": "Summer-Rose",
                "phone": "(376) 893-7556"},
               {"_id": 13,
                "name": "Alton",
                "phone": "(645) 987-9611"}]

user_info.insert_many(sample_info)

sample_mentors = [{"_id": 1,
                   "subjects": ["math", "cs", "history"],
                   "loc": [40.71497363, 73.91207225]},
                  {"_id": 2,
                   "subjects": ["math"],
                   "loc": [40.75821935, 73.99393776]},
                  {"_id": 3,
                   "subjects": ["math"],
                   "loc": [40.68997656, 74.02237431]},
                  {"_id": 5,
                   "subjects": ["math", "cs"],
                   "loc": [40.65571934, 73.99976773]},
                  {"_id": 7,
                   "subjects": ["cs"],
                   "loc": [40.74764641, 74.0672518]},
                  {"_id": 8,
                   "subjects": ["cs", "danse", "math"],
                   "loc": [40.7233218, 74.0905624]},
                  {"_id": 9,
                   "subjects": ["danse", "history"],
                   "loc": [40.75759108, 74.02646335]},
                  {"_id": 10,
                   "subjects": ["math"],
                   "loc": [40.72547593, 73.99582045]},
                  {"_id": 11,
                   "subjects": ["danse"],
                   "loc": [40.66895363, 73.93453277]},
                  {"_id": 13,
                   "subjects": ["danse", "history"],
                   "loc": [40.65173399, 74.01219226]}]

mentor_cache.insert_many(sample_mentors)
mentor_cache.create_index([("loc", pymongo.GEO2D)])