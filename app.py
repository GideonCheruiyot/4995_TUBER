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
requests = {}
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
                self.redirect('/getMentors?_id=' + str(id))
            else:
                self.redirect('/requestQueue?_id=' + str(id))

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
requestIdGenerator = 0

class getMentors(RequestHandler):

    # renders the request page
    def get(self):
        id = self.get_argument('_id')
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
        
        requests[requestIdGenerator] = []
        for mentor in results:
            if mentor['_id'] in mentor_requests.keys():
                mentor_requests[mentor['_id']].append((requestIdGenerator, subject, time, message, student_location))
            else:
                mentor_requests[mentor['_id']] = [(requestIdGenerator, subject, time, message, student_location)]
            requests[requestIdGenerator].append(mentor['_id'])      

        requestIdGenerator += 1
        print(results)
        print(mentor_requests)

        self.redirect('/wait?request_id=' + str(requestIdGenerator - 1) + '&_id=' + str(id))

def updateRequestList(request_id):
    global mentor_requests
    for r in mentor_requests.keys():
        listRequests = mentor_requests[r]
        for req in listRequests:
            if req[0] == request_id:
                listRequests.remove(req)
        mentor_requests[r] = listRequests

class acceptRequest(RequestHandler):

    def post(self):
        id = self.get_body_argument('_id')
        request_id = self.get_argument('request_id')
        releventMentors = requests[request_id]
        
        # update the individual list of relevant requests for each mentor
        updateRequestList(request_id)

        # remove request from the list of open requests
        requests.pop(request_id)
        
        # send message to all relevant mentor to update their request lists
        for mentor in releventMentors:
            if mentor != id:
                opened_sockets[mentor].on_message(mentor_requests[mentor])
        
        self.redirect('/match?_id=' + str(id))

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
            self.redirect('/getMentors?_id=' + str(id))
        else:
            self.redirect('/requestQueue?_id=' + str(id))

class requestQueue(RequestHandler):

    # renders the page with the id in
    # the navigation bar and adds the mentor to the active cache
    def get(self):
        id = int(self.get_argument('_id'))
        IP_to_id_map[id] = self.request.host

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
                       (r'/requestQueue', requestQueue),
                       (r'/acceptRequest', acceptRequest)
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()
