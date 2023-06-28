import gmplot
import csv
import os

path = "C://Users//abrah//Desktop//Project//Data" #path where data is stored

dir_list = os.listdir(path)

gmap1 = gmplot.GoogleMapPlotter.from_geocode("Bridgewater, New Jersey, United States", 15, apikey = 'AIzaSyALPKrX7n5tLMsi0M74X4QY8ppDIEIeSYM')

count = 0 #counter to iterate through colors

color_list = ['blue', 'red', 'purple', 'green', 'orange', 'yellow'] #each color represents different infrastructure piece

for i in dir_list: #goes through every file in the directory and plots the points given, with the name of the file as the name of each point
    with open(path + '//' + i) as f:
        coordinates = []
        for line in f:
            line = line.split()
            if line:           
                line = [float(i) for i in line]
                coordinates.append(line)

    coordinates = zip(*coordinates)

    gmap1.scatter(
         *coordinates,
         color = color_list[count],
         size = 1,
         marker = True, 
         title = i[:i.index(".")]
         )
    count+=1

gmap1.draw("C:\\Users\\abrah\\Desktop\\map.html")

