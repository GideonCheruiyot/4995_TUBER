#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:58:47 2019

@author: red
"""

import pymongo
import dns

co_url = "mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true"
client = pymongo.MongoClient(co_url)
db = client.users
user_info = db.user_info

phone_no = "(636) 403-3675"

def retrieve_id(phone_no):
    query = {"phone": phone_no}
    res = user_info.find_one(query)
    # if no corresponding record in the db
    if res == None:
        return -1
    else:
        _id = res["_id"]
    return _id

print(retrieve_id(phone_no))