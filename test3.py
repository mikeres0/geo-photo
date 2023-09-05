import os
import piexif

def add_or_modify_geolocation(image_path, latitude, longitude):
    try:
        exif_dict = piexif.load(image_path)

        # Convert latitude and longitude to degrees, minutes, seconds format
        def deg_to_dms(deg):
            d = int(deg)
            m = int((deg - d) * 60)
            s = int(((deg - d) * 60 - m) * 60)
            return ((d, 1), (m, 1), (s, 1))

        lat_dms = deg_to_dms(latitude)
        lon_dms = deg_to_dms(longitude)

        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = lat_dms
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = lon_dms
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = 'N' if latitude >= 0 else 'S'
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = 'E' if longitude >= 0 else 'W'

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)

        print("Geolocation data added/modified for", image_path)
    except Exception as e:
        print("Error processing", image_path, ":", e)

def process_images_in_folder(folder_path, latitude, longitude):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            image_path = os.path.join(folder_path, filename)
            add_or_modify_geolocation(image_path, latitude, longitude)

# Example usage
latitude = 34.0522  # Example latitude coordinates
longitude = -118.2437  # Example longitude coordinates
folder_path = 'C:\projects\geo-photo'  # Path to folder containing images

process_images_in_folder(folder_path, latitude, longitude)
