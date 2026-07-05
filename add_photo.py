#!/usr/bin/env python3
import os
import sys
import shutil
import datetime
import subprocess

try:
    import exifread
except ImportError:
    exifread = None

def clear_exif_fields(image_path):
    print(f"Clearing sensitive EXIF fields from {image_path}...")
    try:
        cmd = [
            "exiftool",
            "-overwrite_original",
            "-SerialNumber=",
            "-LensSerialNumber=",
            "-GPS:all=",
            "-OriginalFileName=",
            "-OriginalFilename=",
            "-PreservedFileName=",
            "-Software=",
            "-Artist=",
            "-Creator=",
            "-by-line=",
            image_path
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("EXIF fields cleared successfully.")
    except FileNotFoundError:
        print("Warning: exiftool not found in path, skipping metadata cleaning.", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to clear EXIF metadata: {e.stderr.strip() or e}", file=sys.stderr)

def get_image_date(image_path):
    if exifread is not None:
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                # 'EXIF DateTimeOriginal' is the standard tag
                if 'EXIF DateTimeOriginal' in tags:
                    date_str = str(tags['EXIF DateTimeOriginal'])
                    # Format is typically "YYYY:MM:DD HH:MM:SS"
                    # Extract "YYYY-MM-DD"
                    if len(date_str) >= 10:
                        return date_str[:10].replace(':', '-')
        except Exception as e:
            print(f"Warning: Failed to read EXIF from {image_path}: {e}", file=sys.stderr)
    else:
        print("Warning: exifread module not available, using file creation date.", file=sys.stderr)

    # Fallback to file creation / modification date
    try:
        stat = os.stat(image_path)
        if hasattr(stat, 'st_birthtime'):
            file_time = stat.st_birthtime
        elif os.name == 'nt':
            file_time = stat.st_ctime
        else:
            file_time = stat.st_mtime
        
        dt = datetime.datetime.fromtimestamp(file_time)
        return dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Warning: Failed to get file timestamp: {e}", file=sys.stderr)
        return datetime.date.today().strftime('%Y-%m-%d')

def import_single_photo(image_path):
    # Extract name and extension
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    if not name:
        raise ValueError(f"Could not extract name from file path '{image_path}'")

    target_dir = os.path.join("content", "photos", name)

    if os.path.exists(target_dir):
        raise FileExistsError(f"Directory '{target_dir}' already exists.")

    # Extract date before moving the file
    image_date = get_image_date(image_path)

    # Create directory
    os.makedirs(target_dir)

    # Move image file
    target_image_path = os.path.join(target_dir, base_name)
    try:
        shutil.move(image_path, target_image_path)
    except Exception as e:
        # Attempt cleanup of the directory we just created
        try:
            os.rmdir(target_dir)
        except Exception:
            pass
        raise RuntimeError(f"Failed to move image file to '{target_image_path}': {e}")

    # Clear EXIF fields on target path
    clear_exif_fields(target_image_path)

    # Create index.md
    index_path = os.path.join(target_dir, "index.md")
    try:
        content = f"""---
title: "{name}"
date: {image_date}
tags:
  - "{name}"
---
"""
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully imported photo as page bundle: {target_dir}")
    except Exception as e:
        # Attempt cleanup
        try:
            os.remove(target_image_path)
            os.rmdir(target_dir)
        except Exception:
            pass
        raise RuntimeError(f"Failed to create '{index_path}': {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python add_photo.py <path_to_image_or_directory>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: Path '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(input_path):
        # Gather all *.jpg / *.jpeg files (case-insensitive)
        files = []
        for f in os.listdir(input_path):
            if f.lower().endswith(('.jpg', '.jpeg')):
                files.append(os.path.join(input_path, f))
        
        if not files:
            print(f"No JPG files found in directory '{input_path}'.", file=sys.stderr)
            sys.exit(0)
            
        print(f"Found {len(files)} image files to process.")
        success_count = 0
        fail_count = 0
        for f in sorted(files):
            print(f"\nProcessing {f}...")
            try:
                import_single_photo(f)
                success_count += 1
            except Exception as e:
                print(f"Error importing {f}: {e}", file=sys.stderr)
                fail_count += 1
                
        print(f"\nImport finished. {success_count} succeeded, {fail_count} failed.")
        if fail_count > 0:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        # Single file import
        try:
            import_single_photo(input_path)
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
