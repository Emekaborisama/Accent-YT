from replace_audio_ import replace_audio
from download_video import get_video
from change_audio import SpeechToSpeechConverter
from extract_audio import get_audio
from log_handler import logging
from fastapi import FastAPI, HTTPException, Form, status
from typing import Annotated
from pydantic import BaseModel
from utils import is_valid_youtube_url, get_video_name, move_file_to_folder
import random
import asyncio
import os


XI_API_KEY = os.environ["XI_API_KEY"]
VOICE_ID = os.environ["VOICE_ID"]

converter = SpeechToSpeechConverter(XI_API_KEY, VOICE_ID)


app = FastAPI()


@app.post("/home", summary="Home", description="A welcome message endpoint.")
async def home():
    """
    A simple welcome message.
    """
    return "Welcome"



@app.post("/change_audio", summary="Change yt video audio")
def change_audio_(link: Annotated[str, Form()])-> str:
    uid = random.randint(0,10000)
    try:
        if is_valid_youtube_url(link) == True:
            
            logging.info(f"link is {True}")
            # download audio
            try:
                video_name = get_video_name(link)
                audio_file_path, is_audio_download = get_audio(link=link, video_name = video_name+".mp3", uid=uid)
                video_file_path, is_video_download = get_video(link=link, video_name = video_name, uid=uid)
                logging.info(f"YT saved is {audio_file_path}")
                # print(f"is video download --- s{is_audio_download}, {is_video_download}")
                c_audio_file_path = f"ext_{audio_file_path}"
                converter.convert_speech(input_file_path = audio_file_path, output_file_path=c_audio_file_path)
                video_dest_path = move_file_to_folder(video_file_path, str(uid))
                c_audio_dest_path = move_file_to_folder(c_audio_file_path, str(uid))
                # os.rename(c_audio_dest_path, f"{uid}/{audio_file_path}")
                replace_audio(str(uid))
                # os.remove(audio_file_path)
                return {"uid":uid}
            except Exception as e:
                logging.error(f"private youtube video or cant find the youtube video ---- {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "private youtube video or cant find the youtube video")
            # download video

        else:
            return "input a valid Youtube link"
    except Exception as e:
        logging.error(f"Error processing your request: {e}")



