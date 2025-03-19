import glob
import os
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np

INPUT_DIR = "files"
OUTPUT_DIR = "hymns"
TEMPLATE_PATH = "hymn_template.png"
os.makedirs(OUTPUT_DIR, exist_ok=True)


target_image = cv2.imread(TEMPLATE_PATH)

def mse(imageA, imageB):
    return np.mean((imageA.astype("float") - imageB.astype("float")) ** 2)

def split_out_hymns(input_file, desc):
    CHUNK_LENGTH = 10
    THRESHOLD = 10000
    clip = VideoFileClip(input_file)
    duration = clip.duration

    hymn_names = [chunk.lower() for chunk in desc.split("\n") if "hymn" in chunk.lower()] 
    # strip out hymn and :
    hymn_names = [name.replace("hymn", "").replace(":", "").strip() for name in hymn_names]

    hymn = {}
    index = 0
    is_hymn = False
    hymns = []
    # split duration up into 60 second chunks
    for time in np.arange(0, duration, CHUNK_LENGTH):
        frame = clip.get_frame(time, )
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        resized_target = cv2.resize(target_image, (frame_bgr.shape[1], frame_bgr.shape[0]))
        error = mse(frame_bgr, resized_target)

        if not is_hymn:
            if error < THRESHOLD:
                is_hymn = True
                hymn["start"] = time - CHUNK_LENGTH
                hymn["name"] = hymn_names[index]
        
        if is_hymn:
            if error > THRESHOLD:
                hymn["end"] = time
                hymns.append(hymn)
                is_hymn = False
                index += 1
                hymn = {}
    
    return hymns

def save_hymns(input_file, hymns):
    clip = VideoFileClip(input_file)
    for hymn in hymns:
        start, end = hymn['start'], hymn['end']
        hymn_clip = clip.subclipped(start, end)
        filename = hymn['name'].replace(" ", "_")
        hymn_file_name = os.path.join(OUTPUT_DIR, f"{hymn['name']}.mp4")
        hymn_clip.write_videofile(hymn_file_name, codec='libx264')


def process_urls(input_dir, output_dir):
    files = glob.glob(os.path.join(input_dir, "*.mp4"))
    for video_file in files:
        print(f"Processing {video_file}")

        
        description_file = video_file.replace('.mp4', '_desc.txt')
        description = open(description_file, 'r', encoding='utf-8').read()
        hymns = split_out_hymns(video_file, description)
        save_hymns(video_file, hymns)



# Process all videos
process_urls(INPUT_DIR, OUTPUT_DIR)