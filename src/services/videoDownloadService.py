from pytube import YouTube
import os
from services.loggerServices import setup_logger


logger = setup_logger("videodownloadservice")

def progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_complete = (bytes_downloaded / total_size) * 100
    logger.info(
        f"Downloaded: {bytes_downloaded} / {total_size} bytes ({percentage_complete:.2f}%)")

def downloadYoutubeVideo(url):
    video = YouTube(url, on_progress_callback=progress_callback)
    video_id = video.video_id
    logger.info(f"Downloading video {video_id}")

    stream = video.streams.get_highest_resolution()

    output_path = "videos"

    video_folder = os.path.join(output_path, video_id)
    os.makedirs(video_folder, exist_ok=True)

    video_filename = f"{video_id}.mp4"
    
    video_filepath = os.path.join(video_folder, video_filename)

    stream.download(output_path=video_folder, filename=video_filename, skip_existing=False)
    download_abs_path = os.path.abspath(video_filepath)
    logger.info(f"Downloaded to: {download_abs_path}")
    return download_abs_path