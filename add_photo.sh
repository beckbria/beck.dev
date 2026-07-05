#!/bin/bash
# Exit on error
set -e

if [ -z "$1" ]; then
    echo "Usage: ./add_photo.sh <path_to_image_or_directory>"
    exit 1
fi

# Resolve the absolute path of the input
FILE_PATH=$(realpath "$1")

if [ -f "$FILE_PATH" ]; then
    DIR_PATH=$(dirname "$FILE_PATH")
elif [ -d "$FILE_PATH" ]; then
    DIR_PATH="$FILE_PATH"
else
    echo "Error: Path $FILE_PATH is not a file or directory."
    exit 1
fi

# Detect if sudo is needed to run docker commands
DOCKER_COMPOSE="docker compose"
if command -v docker &>/dev/null; then
    if ! docker ps &>/dev/null; then
        if command -v sudo &>/dev/null; then
            DOCKER_COMPOSE="sudo docker compose"
        fi
    fi
fi

# Run the python script inside the docker container
# We mount the directory containing the files (or the directory itself)
# into the container at the same path.
$DOCKER_COMPOSE run --rm -v "$DIR_PATH:$DIR_PATH" hugo python3 /src/add_photo.py "$FILE_PATH"
