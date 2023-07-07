import streamlit as st
import folium
import pandas as pd
import os
import boto3
import string
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_folium import st_folium
from exif import Image

uri = "mongodb+srv://EagleScout2:KEeIYE07Bj62U0KY@dpwcluster.fkjzh59.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
characters = string.ascii_letters + string.digits

def getCoords(collection):
    database = client.Infrastructure_Data
    coll = eval(collection)
    coordinates = []
    coordinates.append(coll.find({}, {'Latitude': 1, '_id':0}).distinct('Latitude'))
    coordinates.append(coll.find({}, {'Longitude': 1, '_id':0}).distinct('Longitude'))
    return coordinates

StormwaterDrains = getCoords('database.Stormwater_Drains')

StormwaterDrainPoints = pd.DataFrame({
    'lon': StormwaterDrains[1],
    'lat': StormwaterDrains[0]
}, dtype=str)

client.close()

APP_TITLE = 'Infrastructure Map'


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

s3 = boto3.client(
    service_name = 's3',
    region_name = 'us-east-1',
    aws_access_key_id = 'AKIAWDDMU6ABRGHZSOMD',
    aws_secret_access_key = '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'
)

def main():
    st.set_page_config(APP_TITLE)
    st.title(':blue[Map of Infrastructure in the Bridgewater Township]')
    with st.form("myform", clear_on_submit=True):
        file = st.file_uploader(
        label = 'UPLOAD PHOTOS HERE',
        accept_multiple_files = False,
        help = 'Make sure you have location sharing enabled for your camera before taking pictures!',
        )
        infratype = st.selectbox(
            label = 'Please select the type of infrastructure in the image',
            options = ('None', 'Stormwater Drain'),
            help = 'Some infrastructure types may not exist in the database yet'
        )
        submitted = st.form_submit_button("Upload file")
    if submitted and file is None:
        st.error("Please submit a file")
    if submitted and infratype == 'None':
        st.error("Please select the type of infrastructure in the image")
    if submitted and file is not None and infratype != 'None':
        if infratype is 'Stormwater Drain':
            file.name = 'STRM' + ''.join(random.choice(characters) for i in range(25)) + '.jpg'
        with open(os.path.join('c://Users//abrah//Desktop//Project//',file.name), 'wb') as f:
            f.write(file.getbuffer())
        with open('c://Users//abrah//Desktop//Project//' + file.name, 'rb') as src:
            img = Image(src)
        
        if not img.has_exif:
            st.error("This image has no EXIF data, please turn on location services for the camera app before taking pictures to upload")
        else:
            s3.upload_file('c://Users//abrah//Desktop//Project//' + file.name, 'esfilestorage', file.name)
            st.success("Succesfully uploaded file")
    display_map()
        


if __name__ == "__main__":
    main()
