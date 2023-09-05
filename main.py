from PIL import Image
import piexif
from fractions import Fraction

def add_geolocation(image_path, latitude, longitude):
    # Open the image using PIL
    image = Image.open(image_path)

    # Convert latitude and longitude to EXIF format (degrees, minutes, seconds)
    lat_deg = int(latitude)
    lat_min = int((latitude - lat_deg) * 60)
    lat_sec = int(((latitude - lat_deg) * 60 - lat_min) * 60)

    lon_deg = int(longitude)
    lon_min = int((longitude - lon_deg) * 60)
    lon_sec = int(((longitude - lon_deg) * 60 - lon_min) * 60)

    # Create EXIF GPS dictionary
    exif_gps = {
        piexif.GPSIFD.GPSLatitude: (
            (lat_deg, 1),
            (lat_min, 1),
            (lat_sec, 1)
        ),
        piexif.GPSIFD.GPSLongitude: (
            (lon_deg, 1),
            (lon_min, 1),
            (lon_sec, 1)
        ),
        piexif.GPSIFD.GPSLatitudeRef: 'N' if latitude >= 0 else 'S',
        piexif.GPSIFD.GPSLongitudeRef: 'E' if longitude >= 0 else 'W',
    }

    # Add the EXIF GPS data to the image
    exif_dict = {"GPSInfo": exif_gps}
    exif_bytes = piexif.dump(exif_dict)
    image.save("test.jpg", exif=exif_bytes)

    piexif.insert(exif_bytes, image_path)

    print("Geolocation data added to the image.")

if __name__ == "__main__":
    image_path = "test.jpg"  # Path to your JPG image
    latitude = 37.7749  # Example latitude (change to desired value)
    longitude = -122.4194  # Example longitude (change to desired value)

    add_geolocation(image_path, latitude, longitude)