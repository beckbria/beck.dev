#!/usr/bin/env python3
import os
import sys
import subprocess

def clear_exif_fields(image_path):
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
        return True
    except FileNotFoundError:
        print("Error: exiftool not found. Please install exiftool.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error cleaning {image_path}: {e.stderr.strip() or e}", file=sys.stderr)
        return False

def main():
    target_dir = os.path.join("content", "photos")
    if not os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning for images in '{target_dir}' recursively...")
    image_extensions = ('.jpg', '.jpeg', '.png')
    
    image_files = []
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f.lower().endswith(image_extensions):
                image_files.append(os.path.join(root, f))

    if not image_files:
        print("No images found to clean.")
        sys.exit(0)

    print(f"Found {len(image_files)} images. Cleaning metadata...")
    success_count = 0
    fail_count = 0
    
    for idx, path in enumerate(image_files, 1):
        print(f"[{idx}/{len(image_files)}] Cleaning: {path}")
        if clear_exif_fields(path):
            success_count += 1
        else:
            fail_count += 1

    print(f"\nCompleted cleaning. {success_count} succeeded, {fail_count} failed.")
    if fail_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
