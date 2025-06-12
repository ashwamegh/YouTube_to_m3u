#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install dependencies
python3 -m pip install requests

# Run the python script to generate the M3U file
# The python script is in the 'scripts' directory and writes to the root.
python3 scripts/youtube_m3ugrabber.py

echo "M3U file generated."

# Check if there are changes to commit
# --porcelain gives an easy-to-parse output. If it's empty, there are no changes.
if [[ -z $(git status --porcelain) ]]; then
    echo "No changes to commit. Working tree clean."
    exit 0
fi

# Add the generated file, commit and push
echo "Committing and pushing youtube.m3u..."
git add youtube.m3u
git commit -m "Update M3U playlist"
git push
