# importing geopy library
from geopy.geocoders import Nominatim

coord = (26.8393, 80.9321)

geolocator = Nominatim(user_agent='test/1')
location = geolocator.reverse(coord)
print(location.address)