#!/bin/bash
# Exit on error
set -e

# Detect if sudo is needed to run docker commands
DOCKER_COMPOSE="docker compose"
if command -v docker &>/dev/null; then
    if ! docker ps &>/dev/null; then
        if command -v sudo &>/dev/null; then
            DOCKER_COMPOSE="sudo docker compose"
        fi
    fi
fi

# Run clean_exif.py inside the Hugo container
$DOCKER_COMPOSE run --rm hugo python3 /src/clean_exif.py
