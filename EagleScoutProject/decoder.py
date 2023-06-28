import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from GPSPhoto import gpsphoto

#image_list = os.listdir('c:\\Users\\abrah\\Desktop\\Project\\photos')
#image_list = [a for a in image_list if a.endswith('jpg')]
uri = "mongodb+srv://EagleScout2:KEeIYE07Bj62U0KY@dpwcluster.fkjzh59.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1')) # Create a new client and connect to the server

#for a in image_list:
 #   data = gpsphoto.getGPSData(os.getcwd() + '\\photos' + f'\\{a}')
  #  print(data)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!") # Send a ping to confirm a successful connection
except Exception as e:
    print(e)

db = client.Infrastructure_Data
coll = db.Stop_Signs

doc = [
    {"Latitude": 40.6339636, "Longitude":-74.6449061},
]
coll.insert_many(doc)
client.close()