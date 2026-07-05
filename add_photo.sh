#!/bin/bash
# Exit on error
set -e

if [ -z "$1" ]; then
    echo "Usage: ./add_photo.sh <path_to_image>"
    exit 1
fi

# Resolve the absolute path of the input file
FILE_PATH=$(realpath "$1")

if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File $FILE_PATH does not exist."
    exit 1
fi

DIR_PATH=$(dirname "$FILE_PATH")

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
# We mount the directory of the image file into the container at the same path
# so that the container has access to read and move it.
$DOCKER_COMPOSE run --rm -v "$DIR_PATH:$DIR_PATH" hugo python3 /src/add_photo.py "$FILE_PATH"
