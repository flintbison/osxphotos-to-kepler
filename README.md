## About osxphotos-to-kepler
Script to extract metadata directly from the database used by the OSX Photos app   so it can be visualised spatially and temporally in Kepler.gl

## Usage
```sh
python3 osxphotos-to-kepler.py "~/Pictures/Photos Library.photoslibrary"
```

## Default mode

Default mode outputs these metadata properties:
`Filename`  
`DateTime`
`Latitude`
`Longitude`

## Verbose mode (warning   very slow)

```sh
python3 osxphotos-to-kepler.py "~/Pictures/Photos Library.photoslibrary" --verbose
```
Verbose mode outputs these metadata properties:
`UUID`   `Filename`   `OriginalFilename`   `Path`   `PathEdited`   `FileSize`  `FileFormat`   `MediaType`   `DateTime`   `DateAdded`   `DateModified`   `DateTrashed`   `TimezoneOffset`   `Latitude`   `Longitude`   `PlaceName`   `PlaceAddress`   `PlaceCountryCode`   `Title`   `Description`  `Keywords`   `Persons`   `Albums`   `Favorite`   `Hidden`   `Shared`   `Burst`   `BurstSelected`   `Live`   `Portrait`   `HDR`   `HasAdjustments`   `ScoreOverall`   `ScoreCuration`   `ScorePromotion`   `ScoreHighlight`   `ScoreAesthetic`   `ScoreContent`   `Moment`   `OriginalWidth`   `OriginalHeight`   `Width`   `Height`   `Orientation`   `IsCloud`   `InCloud`   `CloudStatus`   `ExternalEdit`   `Project`   `MetadataVersion`