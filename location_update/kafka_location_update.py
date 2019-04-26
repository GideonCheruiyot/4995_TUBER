from kafka import KafkaConsumer
import pymongo
import dns
from bson.son import SON
import ast
import json

client = pymongo.MongoClient("mongodb+srv://tuber-admin:tuber@tubster-qhtny.mongodb.net/test?retryWrites=true")
db = client.users
cache = db.mentor_cache

bulk = cache.initialize_unordered_bulk_op()

consumer = KafkaConsumer('tuber_location_update')

for msg in consumer:
	msg_dict = json.loads(msg.value)
	for key in msg_dict:
		bulk.find({ '_id': int(key) }).update({ '$set': { 'loc': msg_dict[key] } })
		print(key,msg_dict[key])

bulk.execute()
