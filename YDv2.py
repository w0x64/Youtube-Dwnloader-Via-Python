# Youtube updated javascript and also made some other changes so the content grabbed is 360 only. 
# Found a work around with ffmpeg but not releasing anything yet, sorry.


from pytubefix import YouTube, Playlist
import os
import string
import shutil
import getpass
import threading
import sys
import requests
from bs4 import BeautifulSoup
from pytubefix import YouTube as pytubeYouTube # This avoids conflicts with the original YouTube class dont fuck w/ this.

# Grabs the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from pathconfig import DEFAULT_SAVE_PATH
except ImportError:
    # Default to the directory where the script is located if no configuration file is found
    DEFAULT_SAVE_PATH = SCRIPT_DIR

def download_single_video(url, folder_path):
    """ Download a single YouTube video. """
    yt = pytubeYouTube(url)
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    title = ''.join(c for c in yt.title if c in valid_chars)

    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        print("Downloading video...")
        stream.download(output_path=folder_path, filename=f"{title}.mp4")
        print("Download completed!\n")
        return True, title
    else:
        print("No suitable video stream was found.")
        return False, None

def download_playlist(url, folder_path):
    """ Download videos from a YouTube playlist. """
    try:
        p = Playlist(url)
        print(f"Playlist Name : {p.title}\nChannel Name  : {p.owner}\nTotal Videos  : {len(p)}")
    except KeyError:
        # This is youtubes radio token bs.. It extracts playlist URLs when there's a radio token used
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        video_urls = [a['href'] for a in soup.find_all('a', {'class': 'yt-simple-endpoint'})]
        video_urls = ['https://www.youtube.com' + url for url in video_urls]

        print("Playlist Name : Unknown\nChannel Name  : Unknown\nTotal Videos  :", len(video_urls))

        def download_video(video_url, folder_path):
            yt = pytubeYouTube(video_url)
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            title = ''.join(c for c in yt.title if c in valid_chars)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if stream:
                print(f"Downloading: {title}...")
                stream.download(output_path=folder_path, filename=f"{title}.mp4")
                print(f"Download Finished {title}")
            else:
                print(f"No suitable video stream found for {title}")

        print("Downloading Started...")
        print("Please do not close, script is running!")

        threads = []
        for video_url in video_urls:
            thread = threading.Thread(target=download_video, args=(video_url, folder_path))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("Videos Have Been Successfully Downloaded!\n")

        return

    def download_video(video_url, folder_path):
        yt = pytubeYouTube(video_url)
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        title = ''.join(c for c in yt.title if c in valid_chars)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if stream:
            print(f"Downloading: {title}...")
            stream.download(output_path=folder_path, filename=f"{title}.mp4")
            print(f"Download Finished {title}")
        else:
            print(f"No suitable video stream found for {title}")

    print("Downloading Started...")
    print("Please do not close, script is running!")

    threads = []
    for video_url in p.video_urls:
        thread = threading.Thread(target=download_video, args=(video_url, folder_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Videos Have Been Successfully Downloaded!\n")

def main():
    folder_path = DEFAULT_SAVE_PATH

    # The script automatically creates a cache folder which we don't need so I added this to delete it, the folder is named '__pycache__'
    # In the event you wish to inspect the cache folder, remove this part of the script and it will not be purged.
    pycache_path = os.path.join(folder_path, '__pycache__')
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)

    print("Youtube Video Downloader v2\n")

    while True:
        input_url = input('Enter the URL of the YouTube video or playlist: ')

        if 'list=' in input_url:
            download_playlist(input_url, folder_path)
        else:
            success, title = download_single_video(input_url, folder_path)

if __name__ == "__main__":
    main()

# Author:
#                      .oooo.                   .ooo         .o   
#                     d8P'`Y8b                .88'         .d88   
#   oooo oooo    ooo 888    888 oooo    ooo  d88'        .d'888   
#    `88. `88.  .8'  888    888  `88b..8P'  d888P"Ybo. .d'  888   
#     `88..]88..8'   888    888    Y888'    Y88[   ]88 88ooo888oo 
#      `888'`888'    `88b  d88'  .o8"'88b   `Y88   88P      888   
#       `8'  `8'      `Y8bd8P'  o88'   888o  `88bod8'      o888o  
