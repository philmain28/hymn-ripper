# Hymn Ripper

A Python-based tool for downloading and processing hymn videos from YouTube. This tool can:
- Download YouTube videos using yt-dlp
- Extract video descriptions
- Detect and split out individual hymns from longer videos
- Process and save hymns as separate files

## Setup
1. Install dependencies:
```pip install -r requirements.txt```

2. Create a `cookies.txt` file if needed for YouTube authentication

3. Add YouTube URLs to [urls.txt](cci:7://file:///home/philm/Source/hymn_rippin/urls.txt:0:0-0:0)

## Usage
1. Download videos:
```python scripts/youtube_rip.py```

2. Process and split hymns:
```python scripts/process_videos2.py```

## Directory Structure
- `files/`: Downloaded YouTube videos
- `hymns/`: Processed hymn clips
- `scripts/`: Python source code