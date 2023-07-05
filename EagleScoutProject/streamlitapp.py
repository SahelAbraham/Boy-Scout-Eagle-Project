import streamlit as st
import folium
import pandas as pd
import os
import boto3
from PIL import Image
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
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

StormwaterDrains = getCoords('database.Stormwater_Drains')

StormwaterDrainPoints = pd.DataFrame({
    'lon': StormwaterDrains[1],
    'lat': StormwaterDrains[0]
}, dtype=str)

print(StormwaterDrains)
client.close()

APP_TITLE = 'Infrastructure Map'
APP_SUB_TITLE = 'For the Bridgewater Township'


def display_map():
    map = folium.Map(
        location = [40.5940, -74.6049],
        zoom_start = 13,
        tiles= 'cartodbpositron'
    )
    for i in range(0, len(StormwaterDrainPoints)):
        folium.CircleMarker(
            location = [StormwaterDrainPoints.iloc[i]['lat'], StormwaterDrainPoints.iloc[i]['lon']],
            radius = 2,
            color = 'blue',
            tooltip = 'Stop Sign',
            popup = ('Stop Sign' + '\nlatitude:' + StormwaterDrainPoints.iloc[i]['lat'] + '\nlongitude:' + StormwaterDrainPoints.iloc[i]['lon'])
        ).add_to(map)
    st_map = st_folium(
        fig = map,
        height = 700,
        width = 1100
    )

s3 = boto3.resource('s3')

def main():
    st.set_page_config(APP_TITLE)
    st.title(':blue[Infrastructure Map]')
    st.subheader(APP_SUB_TITLE)
    file = st.file_uploader(
        label = 'UPLOAD PHOTOS HERE',
        accept_multiple_files = False,
        help = 'Make sure you have location sharing enabled for your camera before taking pictures!',
    )
    if file is not None:
        file_details = {"Filename":file.name,"FileType":file.type,"FileSize":file.size}
        st.write(file_details)
        with open(os.path.join('c://Users//abrah//Desktop//Project//EagleScoutProject',file.name), 'wb') as f:
            f.write(file.getbuffer())
        s3.meta.client.upload_file('c://Users//abrah//Desktop//Project//EagleScoutProject//IMG_2801.jpg', 'esfilestorage', file.name)
        st.success("Saved File")
    st.button(
        label = 'Refresh Map',
        type = 'primary',
    )
    display_map()
        


if __name__ == "__main__":
    main()
