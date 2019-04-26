from kafka import KafkaProducer
import json


producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),batch_size=0)

locations = {3: [-74.0672519, 40.74764642], 4:[-74.0672519, 40.74764641]}

for key in locations:
	producer.send('tuber_location_update',{key:locations[key]})

producer.close()