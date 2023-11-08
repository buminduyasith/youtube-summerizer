from services.videoDownloadService import downloadYoutubeVideo
import subprocess
import os
from services.loggerServices import setup_logger
import whisper

logger = setup_logger("processVideoService")
url = 'https://www.youtube.com/watch?v=GC80Dk7eg_A'


def convertVideotoAudio(videoPath, audioFilename):
        # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-i', videoPath,
        audioFilename
    ]

        # Run the command
    subprocess.run(command, check=True)
    logger.info("Conversion successful.")
    return True


def processVideo():
    
    absDownloadVideoPath = downloadYoutubeVideo(url)
        
        # Get the video file name without extension
    videoName = os.path.splitext(os.path.basename(absDownloadVideoPath))[0]
            # Create the audio filename with .mp3 extension
    audioFilename = f"{videoName}.mp3"
            
            # Get the directory where the video is located
    video_directory = os.path.dirname(absDownloadVideoPath)
            
            # Construct the full audio filepath
    audioFilepath = os.path.join(video_directory, audioFilename)

    conversionResult = convertVideotoAudio(absDownloadVideoPath, audioFilepath)
    
processVideo();



def createSubtitles(audioFilePath):
    model = whisper.load_model("base")
    result = model.transcribe(audioFilePath)
    return (result["text"])