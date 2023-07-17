from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from fractions import Fraction
import urllib.parse
def format_gps_info(gps_info):
    lat_ref = gps_info.get('GPSLatitudeRef', 'Unknown')
    lon_ref = gps_info.get('GPSLongitudeRef', 'Unknown')

    lat_degrees, lat_minutes, lat_seconds = gps_info.get('GPSLatitude', (0, 0, 0))
    lon_degrees, lon_minutes, lon_seconds = gps_info.get('GPSLongitude', (0, 0, 0))

    # Convert seconds to float
    lat_seconds = float(Fraction(lat_seconds))
    lon_seconds = float(Fraction(lon_seconds))

    # Format latitude and longitude with desired precision (e.g., 6 decimal places)
    latitude = round(lat_degrees + lat_minutes/60 + lat_seconds/3600, 6)
    longitude = round(lon_degrees + lon_minutes/60 + lon_seconds/3600, 6)

    return latitude, longitude

def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geocoding_app")
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
    if location:
        return location.raw
    return None

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data is not None:
            exif_info = {}
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "GPSInfo":
                    gps_info = {}
                    for key in value:
                        sub_tag = GPSTAGS.get(key, key)
                        gps_info[sub_tag] = value[key]
                    exif_info[tag_name] = gps_info
                else:
                    exif_info[tag_name] = value
            return exif_info
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    image_path = "IMG_20230711_185242.jpg"
    exif_data = get_exif_data(image_path)
    if exif_data:
        print("EXIF Data:")
        print("-----------------------------")
        for key, value in exif_data.items():
            if isinstance(key, (int, float)):
                continue  # Skip numeric values
            if key == "GPSInfo":
                latitude, longitude = format_gps_info(value)
                print(f"GPS Latitude: {latitude}")
                print(f"GPS Longitude: {longitude}")
                location_info = get_location_info(latitude, longitude)
                if location_info:
                    print("Location Information:")
                    print("----------------------")
                    for key, value in location_info.items():
                        print(f"{key}: {value}")
                else:
                    print("Reverse geocoding failed.")
                # Build and print the URL with the formatted latitude and longitude
                url = "https://www.google.com/maps/search/?api=1&query="
                url += urllib.parse.quote(str(latitude)) + "," + urllib.parse.quote(str(longitude))
                print("Map URL:", url)
            else:
                print(f"{key}: {value}")
    else:
        print("No EXIF data found in the image.")