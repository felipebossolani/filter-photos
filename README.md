# EXIF Photo Filter

> 🇧🇷 [Leia em Português](README.pt-br.md)

A command-line tool to filter and copy photos based on their **original capture date** (EXIF metadata), not filesystem timestamps.

Useful for recovering photos from old hard drives, external disks, or backups where file creation/modification dates may have changed due to copying between devices.

## Why?

When you copy photos between drives, the filesystem timestamps (`Created`, `Modified`) get overwritten. The only reliable date is the one stored inside the image itself — the EXIF `DateTimeOriginal` field, written by the camera at the moment the photo was taken.

This script reads that field and filters accordingly.

## Requirements

- Python 3.7+
- [Pillow](https://python-pillow.org/)

```bash
pip3 install Pillow
```

For `.heic` files (iPhone photos), also install:

```bash
pip3 install pillow-heif
```

## Usage

```bash
python3 filter_photos.py <source> <dest> [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `source` | Yes | Directory to scan recursively |
| `dest` | Yes | Directory where matched photos will be copied |
| `--start` | No | Start date, inclusive (default: `2011-09-24`) |
| `--end` | No | End date, inclusive (default: `2012-12-31`) |

### Examples

```bash
# Scan an external drive, copy matches to Desktop
python3 filter_photos.py /Volumes/MyDrive/photos ~/Desktop/FilteredPhotos

# Custom date range
python3 filter_photos.py /Volumes/MyDrive/photos ~/Desktop/FilteredPhotos --start 2015-01-01 --end 2015-12-31

# Windows
python3 filter_photos.py E:\photos C:\FilteredPhotos --start 2012-06-01 --end 2012-06-30
```

## Output

The script provides real-time progress with:

- Percentage and file counter
- Running totals for copied, skipped, and errored files
- Elapsed time
- Each matched file logged with its EXIF date

```
Source: /Volumes/ABS-RECOVERY/fotos
Dest:   /Users/you/Desktop/FilteredPhotos
Range:  2015-05-01 to 2015-05-01

Scanning files...
Found 643 image files

  + 2015-05-01 23:07 | IMG_6545.JPG
  + 2015-05-01 23:07 | IMG_6546.JPG
[100.0%] 643/643 | copied: 20 | skipped: 598 | errors: 25 | elapsed: 00:00:09

==================================================
  Done in 00:00:09
  Total scanned:  643
  Copied (match): 20
  Skipped:        598
  Errors:         25
  Output:         /Users/you/Desktop/FilteredPhotos
==================================================
```

## Supported Formats

| Format | EXIF Support |
|--------|-------------|
| `.jpg` / `.jpeg` | Yes — primary use case |
| `.tiff` / `.tif` | Yes |
| `.png` | Rare — most PNGs lack EXIF data |
| `.heic` | Yes — requires `pillow-heif` |

## How It Works

1. Recursively scans the source directory for image files
2. Opens each file and reads the EXIF `DateTimeOriginal` (tag 36867) or `DateTimeDigitized` (tag 36868)
3. If the date falls within the specified range, copies the file to the destination using `shutil.copy2` (preserving metadata)
4. Files without EXIF dates are skipped; corrupted files are logged as errors

## Notes

- **Non-destructive**: the script only copies, never moves or deletes originals
- **Flat output**: all matched files are copied to a single destination folder. Duplicate filenames will be overwritten
- **Corrupted files**: common on old/recovered drives. The `errors` count reflects files that Pillow cannot open — they may be partially recoverable with specialized tools

## License

MIT