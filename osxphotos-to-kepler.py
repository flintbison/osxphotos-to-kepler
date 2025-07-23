import osxphotos
import csv
from datetime import datetime
import argparse
import sys
from tqdm import tqdm
from yaspin import yaspin

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Extract photo metadata and reformat date.')
parser.add_argument('photosdb_path', help='Path to the Photos library database (e.g., ~/Pictures/Photos Library.photoslibrary)')
args = parser.parse_args()

# Output file path
output_file = 'photo_metadata.csv'

# Attempt to initialize PhotosDB and process photos
try:
    # Show spinner for accessing photos db
    with yaspin(text="Accessing photos db...", color="cyan") as spinner:
        photosdb = osxphotos.PhotosDB(args.photosdb_path)
        spinner.ok("✔")
    
    # Show spinner for filtering and sorting photos
    with yaspin(text="Filtering and sorting photos...", color="cyan") as spinner:
        photos = [
            photo for photo in photosdb.photos()
            if photo.date is not None and photo.location is not None
        ]
        photos.sort(key=lambda x: x.date)
        spinner.ok("✔")
    
    # Get total number of photos for progress bar
    total_photos = len(photos)
    print(f"{total_photos} photos found with valid date and location...")
    
    # Write metadata to CSV with reformatted date and additional fields
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Filename", "DateTime", "Latitude", "Longitude", "Created", "Modified",
            "HDR", "Edited", "MediaType", "Description", "Title",
            "PlaceName", "PlaceAddress", "CameraMake", "CameraModel", "LensModel",
            "Score", "Favourite"
        ])
        
        # Use tqdm for progress bar
        for photo in tqdm(photos, total=total_photos, desc="Extracting photo metadata..."):
            filename = photo.original_filename
            # Reformat dates to yyyy-mm-dd hh:mm:ss to be compatible with kepler.gl
            datetime_str = photo.date.strftime("%Y-%m-%d %H:%M:%S") if photo.date else "N/A"
            created_str = photo.date_added.strftime("%Y-%m-%d %H:%M:%S") if photo.date_added else "N/A"
            modified_str = photo.date_modified.strftime("%Y-%m-%d %H:%M:%S") if photo.date_modified else "N/A"
            latitude = photo.location[0] if photo.location else "N/A"
            longitude = photo.location[1] if photo.location else "N/A"
            hdr = photo.hdr
            edited = bool(photo.hasadjustments)
            media_type = photo.media_type if hasattr(photo, 'media_type') else "photo"
            description = photo.description if photo.description else ""
            title = photo.title if photo.title else ""
            place_name = photo.place.name if photo.place and photo.place.name else "N/A"
            place_address = photo.place.address if photo.place and photo.place.address else "N/A"
            # Use exiftool.asdict() for camera metadata
            exif_data = photo.exiftool.asdict() if photo.exiftool else {}
            camera_make = exif_data.get('EXIF:Make', 'N/A')
            camera_model = exif_data.get('EXIF:Model', 'N/A')
            lens_model = exif_data.get('EXIF:LensModel', 'N/A')
            score = photo.score.overall if photo.score and photo.score.overall else 0.0
            favourite = photo.favorite
            
            writer.writerow([
                filename, datetime_str, latitude, longitude, created_str, modified_str,
                hdr, edited, media_type, description, title,
                place_name, place_address, camera_make, camera_model, lens_model,
                score, favourite
            ])
    
    print(f"Processed metadata outputted to: {output_file}")

except Exception as e:
    print(f"Error: Could not access Photos library at '{args.photosdb_path}'.")
    print(f"Details: {str(e)}")
    print("\nUsage: python3 osxphotos-to-kepler.py <path_to_photos_library>")
    print("Example: python3 osxphotos-to-kepler.py \"~/Pictures/Photos Library.photoslibrary\"")
    sys.exit(1)