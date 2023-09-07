import piexif
import os

def add_geolocation(image_path, latitude, longitude):
    exif_dict = piexif.load(image_path)

    # Convert latitude and longitude to degrees, minutes, seconds format
    def deg_to_dms(deg):
        deg = abs(deg)  # Ensure the degree is always positive
        d = int(deg)
        m = int((deg - d) * 60)
        s = ((deg - d) * 60 - m) * 60

        # Handle the case when seconds are close to 60, due to float inaccuracies
        if s >= 59.999:
            s = 0
            m += 1

        # Handle the case when minutes become 60
        if m == 60:
            m = 0
            d += 1

        return ((d, 1), (m, 1), (int(s * 100), 100))

    lat_dms = deg_to_dms(latitude)
    lon_dms = deg_to_dms(longitude)

    print("Latitude DMS:", lat_dms)  # Debugging Line
    print("Longitude DMS:", lon_dms) # Debugging Line

    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = lat_dms
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = lon_dms
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = 'N' if latitude >= 0 else 'S'
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = 'E' if longitude >= 0 else 'W'

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

    print("Geolocation data added to", image_path)

# # Example usage
# latitude = 52.9483758  # Example latitude coordinates
# longitude = -1.1481887  # Example longitude coordinates
# image_path = 'peak.jpg'  # Path to your image

# add_geolocation(image_path, latitude, longitude)


def main():
    folder_path = os.getcwd()
    new_latitude = 52.9483758  # Replace with your desired latitude
    new_longitude = -1.1481887  # Replace with your desired longitude

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            add_geolocation(image_path, new_latitude, new_longitude)

if __name__ == "__main__":
    main()