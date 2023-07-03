import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import folium
from streamlit_folium import st_folium


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

client.close()

APP_TITLE = 'Infrastructure Map'
APP_SUB_TITLE = 'For the Bridgewater Township'


@st.cache_data(experimental_allow_widgets=True)
def display_map():
    map = folium.Map(
        location = [40.5940, -74.6049],
        zoom_start = 14,
        scrollWheelZoom = False,
        tiles= 'cartodbpositron'
    )
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
