#!/usr/bin/python3

banner = r'''
###########################################################################
#      ___    ___    ____                                        	   #
#      \  \  /  /   / /\ \                   			          #
#       \  \/  /   / /__\ \                                               #
#        \    /   / /    \ \                                              #
#         |  |   / /      \ \
#  	  --------------------                                            #
#                                                                         #
#                                  >> https://github.com/UserYahya        #
###########################################################################


'''

import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab_m3u_link(url):
    response = s.get(url, timeout=15).text
    
    if '.m3u8' not in response:
        response = requests.get(url).text
    
    if '.m3u8' not in response:
        return None
    
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        content = response[end-tuner : end]
        if 'https://' in content:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            return link[start : end]
        else:
            tuner += 5
    
    return None

def main():
    global s
    s = requests.Session()
    
    with open('../youtube_channel_info.txt') as f:
        with open('../youtube.m3u', 'w') as output_file:
            print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml.gz"', file=output_file)
            
            for line in f:
                line = line.strip()
                if not line or line.startswith('~~'):
                    continue
                if not line.startswith('https:'):
                    line = line.split('|')
                    ch_name = line[0].strip()
                    grp_title = line[1].strip().title()
                    tvg_logo = line[2].strip()
                    tvg_id = line[3].strip()
                    print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}', file=output_file)
                else:
                    m3u_link = grab_m3u_link(line)
                    if m3u_link:
                        print(m3u_link, file=output_file)
                    else:
                        print(f'https://aasthaott.akamaized.net/110923/smil:bhajan.smil/chunklist_b264000.m3u8', file=output_file)

if __name__ == "__main__":
    main()
