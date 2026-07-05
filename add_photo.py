#!/usr/bin/env python3
import os
import sys
import shutil
import datetime

try:
    import exifread
except ImportError:
    exifread = None

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
        # st_birthtime is the creation date on macOS/BSD and some Linux filesystems.
        # on Windows, st_ctime is the creation time.
        # on Linux without st_birthtime, st_mtime is the modification time.
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python add_photo.py <path_to_image>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Extract name and extension
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    if not name:
        print(f"Error: Could not extract name from file path '{image_path}'", file=sys.stderr)
        sys.exit(1)

    # Define target directory
    # Inside the container, /src is the root of the project.
    target_dir = os.path.join("content", "photos", name)

    if os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' already exists.", file=sys.stderr)
        sys.exit(1)

    # Extract date before moving the file
    image_date = get_image_date(image_path)

    # Create directory
    try:
        os.makedirs(target_dir)
    except Exception as e:
        print(f"Error: Failed to create directory '{target_dir}': {e}", file=sys.stderr)
        sys.exit(1)

    # Move image file
    target_image_path = os.path.join(target_dir, base_name)
    try:
        shutil.move(image_path, target_image_path)
    except Exception as e:
        print(f"Error: Failed to move image file to '{target_image_path}': {e}", file=sys.stderr)
        # Attempt cleanup of the directory we just created
        try:
            os.rmdir(target_dir)
        except Exception:
            pass
        sys.exit(1)

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
        print(f"Error: Failed to create '{index_path}': {e}", file=sys.stderr)
        # Attempt cleanup
        try:
            os.remove(target_image_path)
            os.rmdir(target_dir)
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
