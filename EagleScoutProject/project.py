import gmplot

latitude_list = [ 40.5939636, 40.5940636, 30.3216419 ]
longitude_list = [ -74.6049061, -74.6049061, 78.0413095 ]

gmap1 = gmplot.GoogleMapPlotter.from_geocode("Bridgewater, New Jersey, United States", 15, apikey = 'AIzaSyALPKrX7n5tLMsi0M74X4QY8ppDIEIeSYM')
#gmplot.GoogleMapPlotter(30.3164945, 78.03219179999999, 12, apikey= 'AIzaSyALPKrX7n5tLMsi0M74X4QY8ppDIEIeSYM')

gmap1.scatter( latitude_list, longitude_list, '#FF0000', size = 1, marker = True )

gmap1.draw("C:\\Users\\abrah\\Desktop\\map11.html")

