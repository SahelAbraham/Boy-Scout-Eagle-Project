import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import folium
from streamlit_folium import st_folium
import pandas as pd


uri = "mongodb+srv://EagleScout2:KEeIYE07Bj62U0KY@dpwcluster.fkjzh59.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

def getCoords(collection):
    database = client.Infrastructure_Data
    coll = eval(collection)
    numDocs = coll.count_documents({})
    coordinates = []
    coordinates.append(coll.find({}, {'Latitude': 1, '_id':0}).distinct('Latitude'))
    coordinates.append(coll.find({}, {'Longitude': 1, '_id':0}).distinct('Longitude'))
    return coordinates

StopSigns = getCoords('database.Stop_Signs')
StormwaterDrains = getCoords('database.StormwaterDrains')

#try:
    #StopSigns = pd.DataFrame(getCoords('database.Stop_Signs'), columns = ['latitudes', 'longitudes'])
#except:
    #StopSigns = pd.DataFrame(columns = ['latitudes', 'longitudes'])

#try:
    #StormwaterDrains = pd.DataFrame(getCoords('database.StormwaterDrains'), columns = ['latitudes', 'longitudes'])
#except:
    #StormwaterDrains = pd.DataFrame(columns = ['latitudes', 'longitudes'])

#print(StopSigns)
#print(StormwaterDrains)

StopSignPoints = pd.DataFrame({
    'lon': StopSigns[1],
    'lat': StopSigns[0]
}, dtype=str)

print(StopSignPoints)
client.close()

APP_TITLE = 'Infrastructure Map'
APP_SUB_TITLE = 'For the Bridgewater Township'


def display_map():
    map = folium.Map(
        location = [40.5940, -74.6049],
        zoom_start = 13,
        tiles= 'cartodbpositron'
    )
    for i in range(0, len(StopSignPoints)):
        folium.CircleMarker(
            location = [StopSignPoints.iloc[i]['lat'], StopSignPoints.iloc[i]['lon']],
            radius = 2,
            color = 'red',
            tooltip = 'Stop Sign',
            popup = ('Stop Sign' + '\nlatitude:' + StopSignPoints.iloc[i]['lat'] + '\nlongitude:' + StopSignPoints.iloc[i]['lon'])
        ).add_to(map)
    st_map = st_folium(
        fig = map,
        height = 700,
        width = 1100
    )

def main():
    st.set_page_config(APP_TITLE)
    st.title(':blue[Infrastructure Map]')
    st.subheader(APP_SUB_TITLE)
    st.file_uploader(
        label = 'UPLOAD PHOTOS HERE',
        type = ['png', 'heic'],
        accept_multiple_files = True,
        help = 'Make sure you have location sharing enabled for your camera before taking pictures!',
    )
    st.button(
        label = 'Refresh Map',
        type = 'primary',
    )
    display_map()



if __name__ == "__main__":
    main()
