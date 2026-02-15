from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENCAGE_API_KEY")

def geocode_address(address):       
    geocoder = OpenCageGeocode(API_KEY)
    data = geocoder.geocode(address)
    
    if data and len(data) > 0:
        latitude = data[0]["geometry"]["lat"]
        longitude = data[0]["geometry"]["lng"]
        return latitude, longitude
    else:
        return None, None
