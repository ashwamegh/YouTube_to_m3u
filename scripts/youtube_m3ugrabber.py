#! /usr/bin/python3

import os
import sys
import subprocess

def get_stream_url(youtube_url):
    """
    Get the HLS stream URL for a YouTube live stream with authentication support.
    Uses multiple strategies to bypass YouTube bot detection.
    """
    # Strategy 1: Try with Android player client (bypasses most bot checks)
    try:
        result = subprocess.run(
            [
                'yt-dlp',
                '--no-warnings',
                '--geo-bypass',
                '--extractor-args', 'youtube:player_client=android',
                '-g',
                youtube_url
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            for url in result.stdout.strip().split('\n'):
                if '.m3u8' in url:
                    return url
    except subprocess.TimeoutExpired:
        print(f"Timeout with Android client for {youtube_url}", file=sys.stderr)
    except Exception as e:
        print(f"Android client method failed for {youtube_url}: {e}", file=sys.stderr)
    
    # Strategy 2: Try with web player client
    try:
        result = subprocess.run(
            [
                'yt-dlp',
                '--no-warnings',
                '--geo-bypass',
                '--extractor-args', 'youtube:player_client=web',
                '-g',
                youtube_url
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            for url in result.stdout.strip().split('\n'):
                if '.m3u8' in url:
                    return url
    except subprocess.TimeoutExpired:
        print(f"Timeout with web client for {youtube_url}", file=sys.stderr)
    except Exception as e:
        print(f"Web client method failed for {youtube_url}: {e}", file=sys.stderr)
    
    # Strategy 3: Try with iOS player client as last resort
    try:
        result = subprocess.run(
            [
                'yt-dlp',
                '--no-warnings',
                '--geo-bypass',
                '--extractor-args', 'youtube:player_client=ios',
                '-g',
                youtube_url
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            for url in result.stdout.strip().split('\n'):
                if '.m3u8' in url:
                    return url
    except subprocess.TimeoutExpired:
        print(f"Timeout with iOS client for {youtube_url}", file=sys.stderr)
    except Exception as e:
        print(f"iOS client method failed for {youtube_url}: {e}", file=sys.stderr)
    
    # If all strategies fail, log and return None
    print(f"Failed to extract stream URL for: {youtube_url}", file=sys.stderr)
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