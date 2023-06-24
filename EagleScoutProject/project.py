import gmplot
import csv

latitude_list = []
longitude_list = []

with open('latitudes.csv', newline = '') as f:
    for row in csv.reader(f):
        latitude_list.append(float(row[0]))

with open('longitudes.csv', newline= '') as f:
    for row in csv.reader(f):
        longitude_list.append(float(row[0]))

print(latitude_list)
print(longitude_list)

gmap1 = gmplot.GoogleMapPlotter.from_geocode("Bridgewater, New Jersey, United States", 15, apikey = 'AIzaSyALPKrX7n5tLMsi0M74X4QY8ppDIEIeSYM')
#gmplot.GoogleMapPlotter(30.3164945, 78.03219179999999, 12, apikey= 'AIzaSyALPKrX7n5tLMsi0M74X4QY8ppDIEIeSYM')

gmap1.scatter( latitude_list, longitude_list, '#FF0000', size = 1, marker = True )

gmap1.draw("C:\\Users\\abrah\\Desktop\\map.html")

