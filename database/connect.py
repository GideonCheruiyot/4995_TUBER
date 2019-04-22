#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:48:11 2019

@author: red
"""

import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true")
db = client.test