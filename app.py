import pymongo
import dns
from bson.son import SON

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

# initialize connection to MongoDB and retrieve access to data files
co_url = "mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true"
client = pymongo.MongoClient(co_url)
db = client.users
user_info = db.user_info
cache = db.mentor_cache

# initialize map from IP to id to allow for easy tracking of potential
# mentors to match
IP_to_id_map = {}

class logIn(RequestHandler):

    # render the log in page when launching the app
    def get(self):
        self.render('logIn.html')

    # checking if credentials are correct
    # if not: refreshes the page
    # else: redirects depending on whether the person wants to log in
    # as a mentor or a student (can always change once logged in)
    def post(self):
        which = self.get_body_argument('which')
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
            if which == "student":
                self.redirect('/getMentors?id=' + str(id))
            else:
                self.redirect('/requestQueue?id=' + str(id))


# for the request service search radius: radius: ~1 mile = .017 units
# e.g. here within ~4 miles
radius = .07

class getMentors(RequestHandler):

    # renders the request page adding the id to the navigation bar
    # that allows for changing views
    def get(self):
        id = self.get_argument('id')
        self.render("tutorRequestForm.html", _id=id)

    # fetches the student IP and the content of the request
    # queries the database for potential matches and returns them
    # TO COMPLETE WITH MATCHER SERVICE
    def post(self):
        IP = self.request.host
        subject = self.get_body_argument('subject')
        time  = self.get_body_argument('time')
        message  = self.get_body_argument('message')
        lon = self.get_body_argument('lon')
        lat = self.get_body_argument('lat')
        print('ok')
        print(lon)
        print('fine')
        print(lat)
        student_location = [float(lon), float(lat)]
        query = {"loc": SON([("$near", student_location),
                             ("$maxDistance", radius)]),
                             "subjects": subject}
        prelim = cache.find(query).limit(10)
        results= []

        for res in prelim:
            results.append(res)

        self.redirect('/wait')

# waiting service for student that submitted a request
class wait(RequestHandler):

    def get(self):
        self.render('wait.html')

# service that takes care of switching between mentor and student views
class switchViews(RequestHandler):

    # removes the IP from the active cache if switching from mentor to student
    def post(self):
        to_which = self.get_body_argument('to_which')
        id = self.get_body_argument('_id')
        if to_which == 'student':
            IP_to_id_map.pop(id, None)
            self.redirect('/getMentors?id=' + str(id))
        else:
            self.redirect('/requestQueue?id=' + str(id))

# takes care of what happens on the awaiting mentor page
class requestQueue(RequestHandler):

    # renders the page with the id in
    # the navigation bar and adds the mentor to the active cache
    def get(self):
        id = self.get_argument('id')
        IP_to_id_map[id] = self.request.host
        self.render('mentor.html', _id=id)


if __name__ == "__main__":
    handler_mapping = [
                       (r'/logIn', logIn),
                       (r'/getMentors', getMentors),
                       (r'/wait', wait),
                       (r'/switchViews', switchViews),
                       (r'/requestQueue', requestQueue)
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()
