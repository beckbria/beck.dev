#!/bin/bash

# Exit on error
set -e

ACTION=$1

# Detect if sudo is needed to run docker commands
DOCKER_COMPOSE="docker compose"
if command -v docker &>/dev/null; then
    if ! docker ps &>/dev/null; then
        if command -v sudo &>/dev/null; then
            DOCKER_COMPOSE="sudo docker compose"
        fi
    fi
fi

usage() {
    echo "Usage: ./run.sh <action>"
    echo "Available actions:"
    echo "  dev     - Start local development server at http://localhost:1313"
    echo "  build   - Compile static site to public/ directory"
    echo "  clean   - Remove generated public/ and resources/ files"
    echo "  shell   - Open an interactive shell inside the Hugo container"
    exit 1
}

if [ -z "$ACTION" ]; then
    usage
fi

case "$ACTION" in
    dev)
        echo "Starting local development server..."
        $DOCKER_COMPOSE up
        ;;
    build)
        echo "Building static site (extracting to ./public)..."
        $DOCKER_COMPOSE run --rm hugo hugo --gc --minify
        ;;
    clean)
        echo "Cleaning up build directories..."
        rm -rf public resources
        echo "Clean finished."
        ;;
    shell)
        echo "Entering container shell..."
        $DOCKER_COMPOSE run --rm --entrypoint bash hugo
        ;;
    *)
        usage
        ;;
esac
