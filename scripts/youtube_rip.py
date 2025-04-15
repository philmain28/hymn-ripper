import os
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
#import yt_dlp
#from moviepy.video.fx.all import crop
import re
import yt_dlp
import glob

# Constants
INPUT_FILE = "urls.txt"  # Text file containing YouTube URLs
OUTPUT_DIR = "files"  # Directory to save downloaded videos and metadata
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_youtube_video(url, output_dir):
    """Download a YouTube video using yt-dlp."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Get metadata first to create safe title
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info['title']
        safe_title = re.sub(r'[<>:"/\\|?*()]', '_', video_title)
        safe_title = safe_title.replace(' ', '_')

    # Now download with safe title in output template
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, safe_title + '.%(ext)s'),
        'quiet': True,
        'http_headers': headers,
        'cookies': 'cookies.txt',
        'retries': 3,
        'fragment_retries': 5,
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Check existing files
        existing = check_existing_download(output_dir, safe_title)
        if existing:
            print(f"Already exists: {safe_title}")
            return existing[0], safe_title

        description = info["description"]
        # Clean up and write to file
        description = '\n'.join([line.strip() for line in description.split('\n') if line.strip()])
        with open(os.path.join(output_dir, f"{safe_title}_desc.txt"), 'w', encoding='utf-8') as f:
            f.write(description)
    
        # Download if not found
        ydl.download([url])
        return os.path.join(output_dir, f"{safe_title}.mp4"), safe_title


def check_existing_download(output_dir, video_title):
    """Check if video already exists in output directory."""
    pattern = os.path.join(output_dir, f"{video_title}.*")
    return glob.glob(pattern)


def process_urls(input_file, output_dir):
    """Process all YouTube URLs in the input file."""
    with open(input_file, "r") as file:
        urls = file.read().splitlines()
    
    for url in urls:
        try:
            download_youtube_video(url, output_dir)
        except Exception as e:
            print(f"Download{url} failed with error: {e}")


process_urls(INPUT_FILE, OUTPUT_DIR)
process_urls(INPUT_FILE, OUTPUT_DIR)