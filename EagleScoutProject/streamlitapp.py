import streamlit as st
import folium
import pandas as pd
import os
import boto3
import string
import random
import tempfile
import exifread
import logging as logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_folium import st_folium

#patch used to fix exifread, as the library is broken
def _monkey_patch_exifread():
    from exifread import HEICExifFinder
    from exifread.heic import NoParser

    _old_get_parser = HEICExifFinder.get_parser

    def _get_parser(self, box):
        try:
            return _old_get_parser(self, box)
        except NoParser:
            #logger.warning("ignoring parser %s", box.name)
            return None

    HEICExifFinder.get_parser = _get_parser


_monkey_patch_exifread()

uri = "mongodb+srv://EagleScout2:KEeIYE07Bj62U0KY@dpwcluster.fkjzh59.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
characters = string.ascii_letters + string.digits

def getCoords(collection):
    database = client.Infrastructure_Data
    coll = eval(collection)
    lats = []
    longs = []
    latcursor = coll.find({}, {'Latitude': 1, '_id': 0})
    for row in latcursor:
        for value in row.values():
            lats.append(value)
    longcursor = coll.find({}, {'Longitude': 1, '_id': 0})
    for row in longcursor:
        for value in row.values():
            longs.append(value)
    coordinates = []
    coordinates.append(lats)
    coordinates.append(longs)
    return coordinates

StormwaterDrains = getCoords('database.Stormwater_Drains')
print(str(len(StormwaterDrains[0])) + " latitudes")
print(str(len(StormwaterDrains[1])) + " longitudes")

list1 = [1.2]
list2 = [2.2]
temp = [list1, list2]

StormwaterDrainPoints = pd.DataFrame({
    'lat': StormwaterDrains[0],
    'lon': StormwaterDrains[1]
}, dtype=str)

print(StormwaterDrainPoints)

client.close()

APP_TITLE = 'Infrastructure Map'

s3 = boto3.client(
        service_name = 's3',
        region_name = 'us-east-1',
        aws_access_key_id = 'AKIAWDDMU6ABRGHZSOMD',
        aws_secret_access_key = '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'
    )

# START OF EXIF DATA VERIFICATION
def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon

def get_exif_data(image_file):
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags 

#END OF EXIF DATA VERIFICATION 

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
            tooltip = 'Stormwater Drain',
            popup = ('Stormwater Drain' + '\nlatitude:' + StormwaterDrainPoints.iloc[i]['lat'] + '\nlongitude:' + StormwaterDrainPoints.iloc[i]['lon'])
        ).add_to(map)
    st_map = st_folium(                                                                                                                                  
        fig = map,
        height = 700,
        width = 1100
    )

def generateName():
    return ''.join(random.choice(characters) for i in range(25)) + '.'

def fileUploader(file, infratype, n):
    orgname = file.name
    filetype = file.name.split('.')[-1]
    if infratype == 'Stormwater Drain':
        file.name = 'STRM' + generateName() + filetype
    if infratype == 'TEST':
        file.name = 'TEST' + generateName() + filetype
    upload = True
    with tempfile.TemporaryDirectory() as destination:
        with open(os.path.join(destination,file.name), 'wb') as f:
            f.write(file.getbuffer())
        lat, long = get_exif_location(get_exif_data(os.path.join(destination,file.name)))
        if lat == None or long == None:
            st.error("This image has no exif data, please make sure to turn on location services for the camera app before taking photos to upload")
            upload = False
        elif lat in StormwaterDrains[0] and long in StormwaterDrains[1]:
            st.write("Duplicate image detected")
            upload = False
            print(file.name)
        elif lat in StormwaterDrains[0] or long in StormwaterDrains[1]:
            st.write("Please retake this picture at a different angle")
            upload = False
        if upload == True:
            s3.upload_file(os.path.join(destination,file.name), 'esfilestorage', file.name)
            s3.close()
            print("Finished")
            if n % 10 == 0:
                print(str(n) + " images have been uploaded")
            #st.success("Image has been successfully uploaded to the database!")
        if upload == False:
            print("Did not finish")  

def main():
    st.set_page_config(APP_TITLE)
    st.title(':blue[Map of Infrastructure in the Bridgewater Township]')
    with st.form("myform", clear_on_submit=True):
        files = st.file_uploader(
        label = 'UPLOAD PHOTOS HERE',
        type = ['png', 'jpg', 'jpeg', 'webp', 'heic'],
        accept_multiple_files = True,
        help = 'Make sure you have location sharing enabled for your camera before taking pictures!',
        )
        infra = st.selectbox(   
            label = 'Please select the type of infrastructure in the image',
            options = ('None', 'Stormwater Drain', 'TEST'),
            help = 'Some infrastructure types may not exist in the database yet'
        )
        submitted = st.form_submit_button("Upload file(s)")
    if submitted and files is None:
        st.error("Please submit one or more files")
    if submitted and infra == 'None':
        st.error("Please selectZ the type of infrastructure in the image")
    if submitted and files is not None and infra != 'None':
        n = 1
        for file in files:
            fileUploader(file, infra, n)
            print("Starting")
            n+=1
    display_map()
        


if __name__ == "__main__":
    main()
