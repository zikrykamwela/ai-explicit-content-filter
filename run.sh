#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
. .venv/bin/activate

image_path="${1:-data/test.jpg}"

if [ ! -f "$image_path" ]; then
    echo "Image not found: $image_path"
    echo "Usage: ./run.sh <image-path>"
    exit 1
fi

python run_prediction.py "$image_path"
