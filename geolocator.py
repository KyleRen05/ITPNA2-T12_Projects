from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myApp")
location = geolocator.geocode("Table Mountain, Cape Town")

print(f"Address: {location.address}")
print(f"Latitude: {location.latitude}")
print(f"Longitutde: {location.longitude}")
