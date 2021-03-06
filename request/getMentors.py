from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

import pymongo
import dns
from bson.son import SON

client = pymongo.MongoClient("mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true")
db = client.users
cache = db.mentor_cache

# radius: ~1 mile = .017 units
# e.g. here within ~4 miles
radius = .07

# renders the tutor request form in html
class makeRequest(RequestHandler):
    def get(self):
        self.render("tutorRequestForm.html")

class getMentors(RequestHandler):

    def post(self): 
        subject = self.get_body_argument('subject')
        time  = self.get_body_argument('time')
        message  = self.get_body_argument('message')


    def getMentors(subject, time, message):


    def get(self):

        longitude = self.get_argument('longitude')
        latitude = self.get_argument('latitude')
        # sid = self.get_argument('sid')
        # name = self.get_argument('name')
        # phone = self.get_argument('phone')
        subject = self.get_argument('subject')
        # message = self.get_argument('message')
        student_location = [float(longitude), float(latitude)]
        # self.write('Location recieved')
        # nosql query
        query = {"loc": SON([("$near", student_location), ("$maxDistance", radius)]), "subjects":subject}
        print(query)
        prelim = cache.find(query).limit(10)
        results= []

        for res in prelim:
            results.append(res)
        print(results)
        self.write('\nDone')
        self.finish()




if __name__ == "__main__":
    handler_mapping = [
                       (r'/getMentors', getMentors),
                       (r'/makeRequest', makeRequest)  
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()
