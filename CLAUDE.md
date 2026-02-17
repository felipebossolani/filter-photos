# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file Python CLI tool that filters and copies photos based on EXIF metadata (original capture date), not filesystem timestamps. Used for recovering photos from old drives where file dates may have been altered during copying.

## Running the Script

```bash
# Install dependencies
pip3 install Pillow
pip3 install pillow-heif  # Optional: for HEIC support

# Run with default date range (2011-09-24 to 2012-12-31)
python3 filter_photos.py /path/to/source /path/to/dest

# Run with custom date range
python3 filter_photos.py /path/to/source /path/to/dest --start 2015-01-01 --end 2015-12-31
```

## Architecture

`filter_photos.py` is a standalone script with no modules or dependencies beyond Pillow. The flow is:

1. **Argument parsing** (lines 16-28): Uses argparse for source/dest directories and optional date range
2. **File discovery** (lines 44-48): Recursive walk with extension filter (`.jpg`, `.jpeg`, `.tiff`, `.tif`, `.png`, `.heic`)
3. **EXIF extraction** (lines 68-80): Opens each file with PIL, reads `_getexif()` dictionary
4. **Date filtering** (lines 73-88): Checks EXIF tags 36867 (`DateTimeOriginal`) and 36868 (`DateTimeDigitized`)
5. **File copying** (line 83): Uses `shutil.copy2` to preserve metadata

## Key Implementation Details

- **EXIF tag priority**: Always tries tag 36867 first (DateTimeOriginal), falls back to 36868 (DateTimeDigitized)
- **Date comparison**: END_DATE is set to 23:59:59 (line 28) to make it inclusive
- **Error handling**: Broad exception catch (line 90) counts errors but continues processing
- **Output structure**: Flat directory - all matched files copied to single dest folder, duplicates overwrite
- **Progress display**: Inline status update using `\r` and `flush=True` (line 66)

## Date Format

EXIF dates are stored as strings in format `"YYYY:MM:DD HH:MM:SS"` (note colons in date portion). The script uses `datetime.strptime` with this exact format (line 79).

## Bilingual Documentation

README exists in both English (`README.md`) and Portuguese (`README.pt-br.md`). Keep both in sync when making documentation changes.
