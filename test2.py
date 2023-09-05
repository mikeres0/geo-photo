import piexif

def add_geolocation(image_path, latitude, longitude):
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

    print("Geolocation data added to", image_path)

# Example usage
latitude = 34.0522  # Example latitude coordinates
longitude = -118.2437  # Example longitude coordinates
image_path = 'test.jpg'  # Path to your image

add_geolocation(image_path, latitude, longitude)
