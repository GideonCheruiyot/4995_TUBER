import pymongo
import dns
from bson.son import SON

from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

# initialize connection to MongoDB and retrieve access to data files
co_url = "mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true"
client = pymongo.MongoClient(co_url)
db = client.users
user_info = db.user_info
cache = db.mentor_cache

# initialize map from IP to id to allow for easy tracking of potential
# mentors to match
IP_to_id_map = {}
mentor_requests = {}
opened_sockets = {}

class logIn(RequestHandler):

    # render the log in page when launching the app
    def get(self):
        self.render('logIn.html')

    # checking if credentials are correct
    # if not: refreshes the page
    # else: redirects depending on whether the person wants to log in
    # as a mentor or a student (can always change once logged in)
    def post(self):
        # which = self.get_body_argument('which')
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
            if True:
                self.redirect('/getMentors?id=' + str(id))
            else:
                self.redirect('/requestQueue?id=' + str(id))

class sendMessage(RequestHandler):
    def get(self):
        for os in list(opened_sockets.keys()):
            opened_sockets[os].on_message('Annie')

class sendMessage(RequestHandler):
    def get(self):
        for os in list(opened_sockets.keys()):
            opened_sockets[os].on_message('Annie')

class matcherNotifications(WebSocketHandler):
    def open(self, id):
        opened_sockets[id] = self
        # print('Connection Established.')

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        # close the connection
        # matcherNotifications.opened_sockets.remove(self) 
        pass

	# @classmethod
	# def notify_mentors(cls):
	# 	# get the ip addesses of the intersection of the connected users and the 
		


# for the request service search radius: radius: ~1 mile = .017 units
# e.g. here within ~4 miles
radius = 100

class getMentors(RequestHandler):

    # renders the request page
    def get(self):
        id = self.get_argument('id')
        self.render("tutorRequestForm.html", _id=id)

    # fetches the student IP and the content of the request
    # queries the database for potential matches and returns them
    def post(self):
        IP = self.request.host
        id = self.get_body_argument('_id')
        subject = self.get_body_argument('subject')
        time  = self.get_body_argument('time')
        message  = self.get_body_argument('message')
        # lon = self.get_body_argument('lon')
        # lat = self.get_body_argument('lat')
        lon = -70        
        lat = 43

        student_location = [float(lon), float(lat)]
        query = {"loc": SON([("$near", student_location),
                             ("$maxDistance", radius)]),
                             "subjects": subject}
        prelim = cache.find(query).limit(10)
        results = []

        for res in prelim:
            results.append(res)
        
        for mentor in results:
            if mentor['_id'] in mentor_requests.keys():
                mentor_requests[mentor['_id']].append((subject, time, message, student_location))      
            else:
                mentor_requests[mentor['_id']] = [(subject, time, message, student_location)]

        print(results)
        print(mentor_requests)

        self.redirect('/wait?id=' + str(id))


class wait(RequestHandler):

    def get(self):
        self.render('wait.html')

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

class requestQueue(RequestHandler):

    # renders the page with the id in
    # the navigation bar and adds the mentor to the active cache
    def get(self):
        id = self.get_argument('id')
        IP_to_id_map[id] = self.request.host
        print("mentor reuests keys")
        print(mentor_requests.keys())
        if id in mentor_requests.keys():
            requestList = mentor_requests[id]
        else:
            requestList = []
        self.render('mentor.html', _id=id, requestList=requestList)

if __name__ == "__main__":
    handler_mapping = [
                       (r'/logIn', logIn),
                       (r'/getMentors', getMentors),
                       (r'/wait', wait),
                       (r'/switchViews', switchViews),
                       (r'/sendMessage', sendMessage),
					   (r'/matcherNotifications/(.*)', matcherNotifications),
                       (r'/requestQueue', requestQueue)
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()
