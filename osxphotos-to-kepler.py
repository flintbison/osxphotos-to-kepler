import osxphotos
import csv
from datetime import datetime
import argparse
import sys
from tqdm import tqdm
from yaspin import yaspin
import math
import os

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Extract photo metadata, sort by date, and reformat date.')
parser.add_argument('photosdb_path', help='Path to the Photos library database (e.g., "~/Pictures/Photos Library.photoslibrary")')
parser.add_argument('--verbose', action='store_true', help='Extract all available metadata fields (default: only Filename, DateTime, Latitude, Longitude)')
args = parser.parse_args()

# Output file path
output_file = 'photo_metadata.csv'

# Define common EXIF fields for verbose mode (add more as needed)
exif_fields = [
    'EXIF:Make', 'EXIF:Model', 'EXIF:LensModel', 'EXIF:FocalLength',
    'EXIF:FNumber', 'EXIF:ExposureTime', 'EXIF:ISO', 'EXIF:Orientation',
    'IPTC:Keywords', 'IPTC:Caption-Abstract', 'XMP:TagsList', 'XMP:Subject'
]

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
            if photo.date is not None and
               photo.location is not None and
               isinstance(photo.location[0], (int, float)) and
               isinstance(photo.location[1], (int, float)) and
               not math.isnan(photo.location[0]) and
               not math.isnan(photo.location[1]) and
               -90 <= photo.location[0] <= 90 and
               -180 <= photo.location[1] <= 180
        ]
        photos.sort(key=lambda x: x.date)
        spinner.ok("✔")
    
    # Get total number of photos for progress bar
    total_photos = len(photos)
    print(f"{total_photos} photos found with valid date and location...")
    
    # Write metadata to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        # Define CSV header based on verbose flag
        if args.verbose:
            header = [
                "UUID", "Filename", "OriginalFilename", "Path", "PathEdited", "FileSize",
                "FileFormat", "MediaType", "DateTime", "DateAdded", "DateModified",
                "DateTrashed", "TimezoneOffset", "Latitude", "Longitude", "PlaceName",
                "PlaceAddress", "PlaceCountryCode", "Title", "Description", "Keywords",
                "Persons", "Albums", "Favorite", "Hidden", "Shared", "Burst",
                "BurstSelected", "Live", "Portrait", "HDR", "HasAdjustments",
                "ScoreOverall", "ScoreCuration", "ScorePromotion", "ScoreHighlight",
                "ScoreAesthetic", "ScoreContent", "Moment", "OriginalWidth",
                "OriginalHeight", "Width", "Height", "Orientation", "IsCloud", "InCloud",
                "CloudStatus", "ExternalEdit", "Project", "MetadataVersion"
            ] + exif_fields
        else:
            header = ["Filename", "DateTime", "Latitude", "Longitude"]
        writer.writerow(header)
        
        # Use tqdm for progress bar
        for photo in tqdm(photos, total=total_photos, desc="Extracting photo metadata..."):
            # Common fields for both modes
            filename = photo.original_filename if hasattr(photo, 'original_filename') else "N/A"
            datetime_str = photo.date.strftime("%Y-%m-%d %H:%M:%S") if photo.date else "N/A"
            latitude = photo.location[0]
            longitude = photo.location[1]
            
            # If verbose, extract all fields with hasattr checks
            if args.verbose:
                uuid = photo.uuid if hasattr(photo, 'uuid') else "N/A"
                original_filename = photo.original_filename if hasattr(photo, 'original_filename') else "N/A"
                path = photo.path if hasattr(photo, 'path') and photo.path else "N/A"
                path_edited = photo.path_edited if hasattr(photo, 'path_edited') and photo.path_edited else "N/A"
                file_size = os.path.getsize(photo.path) if hasattr(photo, 'path') and photo.path and os.path.exists(photo.path) else 0
                file_format = photo.uti if hasattr(photo, 'uti') and photo.uti else "N/A"
                media_type = photo.media_type if hasattr(photo, 'media_type') else "photo"
                date_added = photo.date_added.strftime("%Y-%m-%d %H:%M:%S") if hasattr(photo, 'date_added') and photo.date_added else "N/A"
                date_modified = photo.date_modified.strftime("%Y-%m-%d %H:%M:%S") if hasattr(photo, 'date_modified') and photo.date_modified else "N/A"
                date_trashed = photo.date_trashed.strftime("%Y-%m-%d %H:%M:%S") if hasattr(photo, 'date_trashed') and photo.date_trashed else "N/A"
                timezone_offset = photo.timezone_offset if hasattr(photo, 'timezone_offset') else "N/A"
                place_name = photo.place.name if hasattr(photo, 'place') and photo.place and hasattr(photo.place, 'name') and photo.place.name else "N/A"
                place_address = photo.place.address if hasattr(photo, 'place') and photo.place and hasattr(photo.place, 'address') and photo.place.address else "N/A"
                place_country_code = photo.place.country_code if hasattr(photo, 'place') and photo.place and hasattr(photo.place, 'country_code') and photo.place.country_code else "N/A"
                title = photo.title if hasattr(photo, 'title') and photo.title else ""
                description = photo.description if hasattr(photo, 'description') and photo.description else ""
                keywords = ";".join(photo.keywords) if hasattr(photo, 'keywords') and photo.keywords else ""
                persons = ";".join(photo.persons) if hasattr(photo, 'persons') and photo.persons else ""
                albums = ";".join([album.title for album in photo.album_info]) if hasattr(photo, 'album_info') and photo.album_info else ""
                favorite = photo.favorite if hasattr(photo, 'favorite') else False
                hidden = photo.hidden if hasattr(photo, 'hidden') else False
                shared = photo.shared if hasattr(photo, 'shared') else False
                burst = photo.burst if hasattr(photo, 'burst') else False
                burst_selected = photo.burst_selected if hasattr(photo, 'burst_selected') and photo.burst else False
                live = photo.live if hasattr(photo, 'live') else False
                portrait = photo.portrait if hasattr(photo, 'portrait') else False
                hdr = photo.hdr if hasattr(photo, 'hdr') else False
                has_adjustments = photo.hasadjustments if hasattr(photo, 'hasadjustments') else False
                score_overall = photo.score.overall if hasattr(photo, 'score') and photo.score and hasattr(photo.score, 'overall') and photo.score.overall else 0.0
                score_curation = photo.score.curation if hasattr(photo, 'score') and photo.score and hasattr(photo.score, 'curation') and photo.score.curation else 0.0
                score_promotion = photo.score.promotion if hasattr(photo, 'score') and photo.score and hasattr(photo.score, 'promotion') and photo.score.promotion else 0.0
                score_highlight = photo.score.highlight if hasattr(photo, 'score') and photo.score and hasattr(photo.score, 'highlight') and photo.score.highlight else 0.0
                score_aesthetic = photo.score.aesthetic if hasattr(photo, 'score') and photo.score and hasattr(photo.score, 'aesthetic') and photo.score.aesthetic else 0.0
                score_content = photo.score.content if hasattr(photo, 'score') and photo.score and hasattr(photo.score, 'content') and photo.score.content else 0.0
                moment = photo.moment if hasattr(photo, 'moment') else "N/A"
                original_width = photo.original_width if hasattr(photo, 'original_width') and photo.original_width else 0
                original_height = photo.original_height if hasattr(photo, 'original_height') and photo.original_height else 0
                width = photo.width if hasattr(photo, 'width') and photo.width else 0
                height = photo.height if hasattr(photo, 'height') and photo.height else 0
                orientation = photo.orientation if hasattr(photo, 'orientation') and photo.orientation else 0
                is_cloud = photo.is_cloud if hasattr(photo, 'is_cloud') else False
                in_cloud = photo.in_cloud if hasattr(photo, 'in_cloud') else False
                cloud_status = photo.cloud_status if hasattr(photo, 'cloud_status') else "N/A"
                external_edit = photo.external_edit if hasattr(photo, 'external_edit') else False
                project = photo.project if hasattr(photo, 'project') else "N/A"
                metadata_version = photo.metadata_version if hasattr(photo, 'metadata_version') else "N/A"
                exif_data = photo.exiftool.asdict() if hasattr(photo, 'exiftool') and photo.exiftool else {}
                exif_values = [exif_data.get(field, "N/A") for field in exif_fields]
                
                row = [
                    uuid, filename, original_filename, path, path_edited, file_size,
                    file_format, media_type, datetime_str, date_added, date_modified,
                    date_trashed, timezone_offset, latitude, longitude, place_name,
                    place_address, place_country_code, title, description, keywords,
                    persons, albums, favorite, hidden, shared, burst, burst_selected,
                    live, portrait, hdr, has_adjustments, score_overall, score_curation,
                    score_promotion, score_highlight, score_aesthetic, score_content,
                    moment, original_width, original_height, width, height, orientation,
                    is_cloud, in_cloud, cloud_status, external_edit, project, metadata_version
                ] + exif_values
            else:
                row = [filename, datetime_str, latitude, longitude]
            
            writer.writerow(row)
    
    print(f"Processed metadata outputted to: {output_file}")

except Exception as e:
    print(f"Error: Could not access Photos library at '{args.photosdb_path}'.")
    print(f"Details: {str(e)}")
    print("\nUsage: python3 osxphotos-to-kepler.py <path_to_photos_library> [--verbose]")
    print("Example: python3 osxphotos-to-kepler.py \"~/Pictures/Photos Library.photoslibrary\"")
    print("Example (verbose): python3 osxphotos-to-kepler.py \"~/Pictures/Photos Library.photoslibrary\" --verbose")
    sys.exit(1)