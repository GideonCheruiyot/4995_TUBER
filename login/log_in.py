#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:58:47 2019

@author: red
"""

import pymongo
import dns

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

co_url = "mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true"
client = pymongo.MongoClient(co_url)
db = client.users
user_info = db.user_info

class logIn(RequestHandler):

    def get(self):


    def post(self):
        name = self.get_body_argument('username')
        password = self.get_body_argument('password')
        id = retrieve_id(name)
        if (id != -1):
            self.redirect('/makeRequest')
        else:
            self.write("/nTry again! No matches were found")

    def retrieve_id(username):
        query = {"username": username}
        res = user_info.find_one(query)
        # if no corresponding record in the db
        if res == None:
            return -1
        else:
            _id = res["_id"]
        return _id


if __name__ == "__main__":
    handler_mapping = [
                       (r'/log_in', logIn),
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()
