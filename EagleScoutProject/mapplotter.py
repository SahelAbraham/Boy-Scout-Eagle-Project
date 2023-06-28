import gmplot
import csv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://EagleScout2:KEeIYE07Bj62U0KY@dpwcluster.fkjzh59.mongodb.net/?retryWrites=true&w=majority"
gmap1 = gmplot.GoogleMapPlotter.from_geocode("Bridgewater, New Jersey, United States", 15, apikey = 'AIzaSyALPKrX7n5tLMsi0M74X4QY8ppDIEIeSYM')

client = MongoClient(uri, server_api=ServerApi('1')) # Create a new client and connect to the server

database = client.Infrastructure_Data
coll = database.Stop_Signs
numDocs = coll.count_documents({})
coordinates = []
coordinates.append(coll.find({}, {'Latitude': 1, '_id':0}).distinct('Latitude'))
coordinates.append(coll.find({}, {'Longitude': 1, '_id':0}).distinct('Longitude'))
print(coordinates)


client.close()

gmap1.scatter(
    *coordinates,
    color = 'blue',
    size = 1,
    marker = True, 
    title = 'Stop Sign'
)

gmap1.draw("C:\\Users\\abrah\\Desktop\\map.html")

