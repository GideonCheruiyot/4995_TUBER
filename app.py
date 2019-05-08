import pymongo
import dns
from bson.son import SON

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

co_url = "mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true"
client = pymongo.MongoClient(co_url)
db = client.users
user_info = db.user_info
cache = db.mentor_cache

id = 0

class logIn(RequestHandler):

    def get(self):
        self.render('logIn.html')

    def post(self):
        global id
        name = self.get_body_argument('username')
        password = self.get_body_argument('password')
        query = {"username": name, "password": password}
        res = user_info.find_one(query)
        #if no corresponding record in the db
        if res is None:
            id = -1
            self.redirect('/logIn')
        else:
            id = res["_id"]
            self.redirect('/getMentors?id=' + str(id))


# radius: ~1 mile = .017 units
# e.g. here within ~4 miles
radius = .07

class getMentors(RequestHandler):

    id = 0

    def get(self):
        global id
        id = self.get_argument('id')
        self.render("tutorRequestForm.html")

    def post(self):
        subject = self.get_body_argument('subject')
        time  = self.get_body_argument('time')
        message  = self.get_body_argument('message')
        lon = self.get_body_argument('lon')
        lat = self.get_body_argument('lat')
        student_location = [float(lon), float(lat)]
        query = {"loc": SON([("$near", student_location),
                             ("$maxDistance", radius)]),
                             "subjects": subject}
        prelim = cache.find(query).limit(10)
        results= []

        for res in prelim:
            results.append(res)

        self.redirect('/wait?id=' + str(id))

class wait(RequestHandler):

    def get(self):
        self.render('wait.html')

class switchViews(RequestHandler):

    def get(self):
        to_which = self.get_argument('to_which')
        if to_which == 'student':
            self.redirect('/getMentors')
        else:
            t = 0
            #self.redirect('/requestQueue')

if __name__ == "__main__":
    handler_mapping = [
                       (r'/logIn', logIn),
                       (r'/getMentors', getMentors),
                       (r'/wait', wait),
                       (r'/switchViews', switchViews)
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()
