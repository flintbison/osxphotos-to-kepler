import osxphotos
import csv
from datetime import datetime
import argparse
import sys
from tqdm import tqdm

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Extract photo metadata and reformat date.')
parser.add_argument('photosdb_path', help='Path to the Photos library database (e.g., ~/Pictures/Photos Library.photoslibrary)')
args = parser.parse_args()

# Output file path
output_file = 'photo_metadata.csv'

# Attempt to initialize PhotosDB and process photos
try:
    # Print message at commandline to tell user that access to photos has begun
    print(f"Accessing photos db...")

    photosdb = osxphotos.PhotosDB(args.photosdb_path)    
    
    # Get total number of photos for progress bar
    total_photos = len(photosdb.photos())

    # Print message at commandline to tell user how many photos have been found in db
    print(f"{total_photos} photos found...")

    # Print message at commandline to tell user that processing of photos in underway
    print(f"Processing...")
    
    # Write metadata to CSV with reformatted date
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "DateTime", "Latitude", "Longitude"])
        
        # Use tqdm for progress bar
        for photo in tqdm(photosdb.photos(), total=total_photos, desc="Extracting photo metadata..."):
            filename = photo.original_filename
            # Extract and reformat date to yyyy-mm-dd hh:mm:ss
            datetime_str = photo.date.strftime("%Y-%m-%d %H:%M:%S") if photo.date else "N/A"
            latitude = photo.location[0] if photo.location else "N/A"
            longitude = photo.location[1] if photo.location else "N/A"
            writer.writerow([filename, datetime_str, latitude, longitude])
    
    print(f"Metadata extracted and reformatted to {output_file}")

except Exception as e:
    print(f"Error: Could not access Photos library at '{args.photosdb_path}'.")
    print(f"Details: {str(e)}")
    print("\nUsage: python3 osxphotos-to-kepler.py <path_to_photos_library>")
    print("Example: python3 osxphotos-to-kepler.py ~/Pictures/Photos Library.photoslibrary")
    sys.exit(1)