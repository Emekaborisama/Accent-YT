import logging
from log_handler import logging
# from subprocess import run
from subprocess_tee import run
from utils import rename_file 

def get_video(link:str, video_name: str, uid: int):
    logging.info(f"Starting download for link: {link}")
    try:
        result = run(f"ytb_downloader  -f 'mp4' --video-only '{link}'  ")
        logging.info("Download completed successfully.")
        logging.debug(f"Command output: {result.stdout}")
        path = rename_file(video_name, "mp4", uid)
        if result.stderr:
            logging.warning(f"Command produced errors: {result.stderr}")
            return path, True

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        path = rename_file(video_name, "mp4", uid)
        return path, False