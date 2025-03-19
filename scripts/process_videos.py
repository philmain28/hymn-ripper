import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import glob
import cv2
import numpy as np
from scenedetect.detectors import HistogramDetector, AdaptiveDetector
from scenedetect import detect, open_video



# Constants
INPUT_DIR = "files"
OUTPUT_DIR = "processed_files"
TEMPLATE_PATH = "hymn_template.png"
os.makedirs(OUTPUT_DIR, exist_ok=True)



# split file using pyscenedetect

def scene_detection(video_file, output_dir):
    scene_list = detect(
        video_file, 
        #HistogramDetector(threshold=0.1),
        AdaptiveDetector(),
        stats_file_path= "stats.txt",
        show_progress=True,
        end_time = "00:15:00"
    )
    for i, scene in enumerate(scene_list):
        print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
            i+1,
            scene[0].get_timecode(), scene[0].get_frames(),
            scene[1].get_timecode(), scene[1].get_frames(),))

    return scene_list


# Function to process all video files in the input directory
def process_urls(input_dir, output_dir):
    files = glob.glob(os.path.join(input_dir, "*.mp4"))
    for video_file in files:
        print(f"Processing {video_file}")
        #times = process_video(video_file, output_dir)  # Updated function name
        times = scene_detection(video_file, output_dir)
        print(f"Found {len(times)} matching times")

# Process all videos
process_urls(INPUT_DIR, OUTPUT_DIR)