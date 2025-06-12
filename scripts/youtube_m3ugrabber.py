#! /usr/bin/python3

import os
import sys
import subprocess

def get_stream_url(youtube_url):
    """
    Uses yt-dlp to get the HLS stream URL. Returns None on failure.
    """
    try:
        result = subprocess.run(
            ['yt-dlp', '-g', '--no-warnings', youtube_url],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        for url in result.stdout.strip().split('\n'):
            if url.endswith('.m3u8'):
                return url
        # If loop finishes, no .m3u8 stream was found
        print(f"Warning: No .m3u8 stream found for {youtube_url}", file=sys.stderr)
        return None
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        # yt-dlp returns non-zero for non-live videos, which is expected.
        print(f"Info: Could not get stream for {youtube_url}. It might not be live.", file=sys.stderr)
        return None

def main():
    info_file_path = '../youtube_channel_info.txt'

    print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml.gz"')
    
    with open(info_file_path) as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('~~')]

    i = 0
    while i < len(lines):
        # Expect a channel info line, which does not start with https
        channel_info_line = lines[i]
        if channel_info_line.startswith('https:'):
            # This is a URL without channel info, skip
            i += 1
            continue
            
        # Expect a URL line next
        if (i + 1) < len(lines) and lines[i+1].startswith('https:'):
            youtube_url = lines[i+1]
            
            stream_url = get_stream_url(youtube_url)
            
            # Only print the entry if we get a valid stream URL
            if stream_url:
                try:
                    line_parts = channel_info_line.split('|')
                    ch_name = line_parts[0].strip()
                    grp_title = line_parts[1].strip().title()
                    tvg_logo = line_parts[2].strip()
                    tvg_id = line_parts[3].strip()
                    print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
                    print(stream_url)
                except IndexError:
                    print(f"Warning: Malformed channel info line, skipping: {channel_info_line}", file=sys.stderr)

            # Move past the pair of lines we've processed
            i += 2
        else:
            # Malformed entry (e.g., info line not followed by URL), skip the info line.
            i += 1

if __name__ == "__main__":
    main()