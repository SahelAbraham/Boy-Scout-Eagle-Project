import os

image_list = os.listdir('c:\\Users\\abrah\\Desktop\\Project\\photos')
image_list = [a for a in image_list if a.endswith('jpg')]

from GPSPhoto import gpsphoto
for a in image_list:
    data = gpsphoto.getGPSData(os.getcwd() + '\\photos' + f'\\{a}')
    print(data)

