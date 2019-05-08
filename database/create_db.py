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
                "phone": "(636) 403-3645",
                "username": "edd",
                "password": "edd"},
               {"_id": 2,
                "name": "Finbar",
                "phone": "(511) 798-7872",
                "username": "fbar",
                "password": "foo"},
               {"_id": 3,
                "name": "Cassius",
                "phone": "(598) 811-0301",
                "username": "cassiuuus",
                "password": "cassy"},
               {"_id": 4,
                "name": "Fahmida",
                "phone": "(204) 460-4466",
                "username": "fahm",
                "password": "yup"},
               {"_id": 5,
                "name": "Maud",
                "phone": "(250) 828-4040",
                "username": "fashionmode",
                "password": "realmaud"},
               {"_id": 6,
                "name": "Rebekka",
                "phone": "(422) 567-7496",
                "username": "becky",
                "password": "funfunfun"},
               {"_id": 7,
                "name": "Armaan",
                "phone": "(215) 919-7472",
                "username": "armaan",
                "password": "armaan"},
               {"_id": 8,
                "name": "Vivek",
                "phone": "(642) 741-5072",
                "username": "vivek",
                "password": "vivek"},
               {"_id": 9,
                "name": "Donna",
                "phone": "((448) 622-9390",
                "username": "donnawholelottawork",
                "password": "donna"},
               {"_id": 10,
                "name": "Lilly-Mai",
                "phone": "(383) 337-9449",
                "username": "liliesarepretty",
                "password": "mai"},
               {"_id": 11,
                "name": "Maddox",
                "phone": "(930) 882-4251",
                "username": "maddie",
                "password": "123"},
               {"_id": 12,
                "name": "Summer-Rose",
                "phone": "(376) 893-7556",
                "username": "sum",
                "password": "rose"},
               {"_id": 13,
                "name": "Alton",
                "phone": "(645) 987-9611",
                "username": "alt",
                "password": "alt"}]

user_info.insert_many(sample_info)

# need longitude first
sample_mentors = [{"_id": 1,
                   "subjects": ["math", "cs", "history"],
                   "loc": [-73.91207225, 40.71497363]},
                  {"_id": 2,
                   "subjects": ["math"],
                   "loc": [-73.99393776, 40.75821935]},
                  {"_id": 3,
                   "subjects": ["math"],
                   "loc": [-74.02237431, 40.68997656]},
                  {"_id": 5,
                   "subjects": ["math", "cs"],
                   "loc": [-73.99976773, 40.65571934]},
                  {"_id": 7,
                   "subjects": ["cs"],
                   "loc": [-74.0672518, 40.74764641]},
                  {"_id": 8,
                   "subjects": ["cs", "dance", "math"],
                   "loc": [-74.0905624, 40.7233218]},
                  {"_id": 9,
                   "subjects": ["dance", "history"],
                   "loc": [-74.02646335, 40.75759108]},
                  {"_id": 10,
                   "subjects": ["math"],
                   "loc": [-73.99582045, 40.72547593]},
                  {"_id": 11,
                   "subjects": ["dance"],
                   "loc": [-73.93453277, 40.66895363]},
                  {"_id": 13,
                   "subjects": ["dance", "history"],
                   "loc": [-74.01219226, 40.65173399]}]

mentor_cache.insert_many(sample_mentors)
mentor_cache.create_index([("loc", pymongo.GEO2D)])
