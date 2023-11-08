from services.videoDownloadService import downloadYoutubeVideo
import subprocess
import os
from services.loggerServices import setup_logger
import whisper
import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
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

    videoName = os.path.splitext(os.path.basename(absDownloadVideoPath))[0]

    audioFilename = f"{videoName}.mp3"

    video_directory = os.path.dirname(absDownloadVideoPath)

    audioFilepath = os.path.join(video_directory, audioFilename)

    conversionResult = convertVideotoAudio(absDownloadVideoPath, audioFilepath)

    contentInText = audioToText(audioFilepath)
    
    summerizeContent = summerizeContent(contentInText)
    
    print(summerizeContent)


def audioToText(audioFilePath):
    model = whisper.load_model("base")
    result = model.transcribe(audioFilePath)
    return (result["text"])


def summerizeContent(content):

    openai_api_key = os.getenv('OPENAPI_KEY')
    chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

    messages = [
        SystemMessage(
            content="You are a helpful assistant that summarizes various types of educational content. When you summarize, you focus on the most important facts that might be asked in exams, presenting them in a concise, point-form format."
        ),
        HumanMessage(
            content=content
        ),
    ]

    summerizeContent = chat(messages)
    print(summerizeContent)