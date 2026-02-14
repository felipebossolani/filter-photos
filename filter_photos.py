import os
import sys
import shutil
import time
import argparse
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow first: pip3 install Pillow")
    sys.exit(1)

# Args
parser = argparse.ArgumentParser(
    description="Filter photos by EXIF date range. Scans source directory recursively and copies matching photos to destination."
)
parser.add_argument("source", help="Source directory to scan")
parser.add_argument("dest", help="Destination directory for matched photos")
parser.add_argument("--start", default="2011-09-24", help="Start date inclusive (YYYY-MM-DD, default: 2011-09-24)")
parser.add_argument("--end", default="2012-12-31", help="End date inclusive (YYYY-MM-DD, default: 2012-12-31)")
args = parser.parse_args()

SOURCE = args.source
DEST = args.dest
START_DATE = datetime.strptime(args.start, "%Y-%m-%d")
END_DATE = datetime.strptime(args.end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
EXTENSIONS = {".jpg", ".jpeg", ".tiff", ".tif", ".png", ".heic"}

if not os.path.isdir(SOURCE):
    print(f"Error: source directory not found: {SOURCE}")
    sys.exit(1)

os.makedirs(DEST, exist_ok=True)

# Scan files
print(f"Source: {SOURCE}")
print(f"Dest:   {DEST}")
print(f"Range:  {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
print()
print("Scanning files...")

files = []
for root, _, filenames in os.walk(SOURCE):
    for f in filenames:
        if Path(f).suffix.lower() in EXTENSIONS:
            files.append(os.path.join(root, f))

total_files = len(files)
print(f"Found {total_files} image files\n")

if total_files == 0:
    print("Nothing to process.")
    sys.exit(0)

matched = 0
skipped = 0
errors = 0
start_time = time.time()

for i, filepath in enumerate(files, 1):
    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    pct = round((i / total_files) * 100, 1)
    status = f"\r[{pct}%] {i}/{total_files} | copied: {matched} | skipped: {skipped} | errors: {errors} | elapsed: {elapsed}"
    print(status, end="", flush=True)

    try:
        img = Image.open(filepath)
        exif = img._getexif()
        img.close()

        date_taken = None
        if exif:
            # 36867 = DateTimeOriginal, 36868 = DateTimeDigitized
            for tag_id in (36867, 36868):
                if tag_id in exif:
                    date_str = exif[tag_id]
                    date_taken = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    break

        if date_taken and START_DATE <= date_taken <= END_DATE:
            shutil.copy2(filepath, DEST)
            matched += 1
            print()
            print(f"  + {date_taken.strftime('%Y-%m-%d %H:%M')} | {os.path.basename(filepath)}")
        else:
            skipped += 1

    except Exception as e:
        errors += 1
        print()
        print(f"  ! Error: {os.path.basename(filepath)} - {e}")

elapsed_final = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))

print("\n")
print("=" * 50)
print(f"  Done in {elapsed_final}")
print(f"  Total scanned:  {total_files}")
print(f"  Copied (match): {matched}")
print(f"  Skipped:        {skipped}")
print(f"  Errors:         {errors}")
print(f"  Output:         {DEST}")
print("=" * 50)