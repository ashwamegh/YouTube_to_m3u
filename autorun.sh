#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install requests yt-dlp

# Add Python user bin directory to PATH to ensure yt-dlp is found
export PATH="$(python3 -m site --user-base)/bin:$PATH"

# Navigate to the script directory
cd "$(dirname "$0")/scripts"

# Run the python script to generate the M3U file
echo "Generating M3U file..."
python3 youtube_m3ugrabber.py > ../youtube.m3u
echo "M3U file generated."

# Navigate back to the repo root to perform git operations
cd ..

# Check if there are changes to commit
if [[ -z $(git status --porcelain youtube.m3u) ]]; then
    echo "No changes to youtube.m3u. Working tree clean."
    exit 0
fi

# Add the generated file, commit and push
echo "Committing and pushing youtube.m3u..."
git add youtube.m3u
git commit -m "Update M3U playlist"
git push