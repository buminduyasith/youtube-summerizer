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

def downlonYoutubeVideo(url):
    video = YouTube(url, on_progress_callback=progress_callback)
    video_id = video.video_id  # Get the YouTube video ID
    logger.info(f"Downloading video {video_id}")

    # Choose the stream with the highest resolution
    stream = video.streams.get_highest_resolution()

    # Specify the directory where you want to save the video
    output_path = "videos"  # Replace with the actual path

    # Use the video ID as the folder name
    video_folder = os.path.join(output_path, video_id)
    os.makedirs(video_folder, exist_ok=True)

    # Use the video ID as the filename
    video_filename = f"{video_id}.mp4"
    
    # Construct the full path to the video file
    video_filepath = os.path.join(video_folder, video_filename)

    # Download the video to the specified directory with the video filename
    stream.download(output_path=video_folder, filename=video_filename, skip_existing=False)
    download_abs_path = os.path.abspath(video_filepath)
    logger.info(f"Downloaded to: {download_abs_path}")
    return download_abs_path

downlonYoutubeVideo('https://www.youtube.com/watch?v=GC80Dk7eg_A')