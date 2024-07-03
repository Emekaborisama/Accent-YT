import re
import urllib.request
import json
import urllib
import os
import re
import logging
import shutil


def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=|.+/)?'
        '([a-zA-Z0-9_-]{11})'
    )
    
    return youtube_regex.match(url) is not None


def get_video_name(link:str):
    result = ""
    params = {"format": "json", "url": link}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        # pprint.pprint(data)
        result+= data['title']
    return result

def clean_file_name(file_name):
    # Remove unwanted characters and replace spaces with underscores
    cleaned_name = re.sub(r'[^\w\s-]', '', file_name)  # Remove special characters except spaces and hyphens
    cleaned_name = re.sub(r'\s+', '_', cleaned_name)  # Replace spaces with underscores
    result = cleaned_name.lower()
    return result

def rename_file(file_name, file_ext, uid:int):
    # Get full path of the file
    directory = os.getcwd()
    file_path = os.path.join(directory, file_name)
    
    # Ensure it's a file (not a directory)
    if os.path.isfile(file_path):
        # Split the file name and extension
        name, ext = os.path.splitext(file_name)
        # Clean the file name
        cleaned_name = clean_file_name(name)
        # Construct the new file name with the same extension
        new_file_name = f"{cleaned_name}_{uid}.{file_ext}"
        # Get the full path of the new file name
        new_file_path = os.path.join(directory, new_file_name)
        
        # Rename the file
        os.rename(file_path, new_file_path)
        return new_file_name
    else:
        return None

    

def move_file_to_folder(src_file_path:str, dest_folder_path):
    try:
        # Ensure the source file exists
        if not os.path.isfile(src_file_path):
            logging.info(f"Source file not found: {src_file_path}")
            return

        # Ensure the destination folder exists, create if not
        if not os.path.exists(dest_folder_path):
            os.makedirs(dest_folder_path)

        # Extract the file name from the source file path
        file_name = os.path.basename(src_file_path)
        # Construct the destination file path
        dest_file_path = os.path.join(dest_folder_path, file_name)

        # Move the file
        shutil.move(src_file_path, dest_file_path)

        logging.info(f"Moved file to the destination folder _ {dest_file_path}")
        return dest_file_path
    except Exception as e:
        logging.error(f"Couldn't move file to the destination folder _ {e}")



# def move_file_to_folder(src_file_path:list, dest_folder_path):
#     try:
#         des_result = ""
#         for x in src_file_path:
#             # Ensure the source file exists
#             if not os.path.isfile(src_file_path):
#                 logging.info(f"Source file not found: {src_file_path}")
#                 return

#             # Ensure the destination folder exists, create if not
#             if not os.path.exists(dest_folder_path):
#                 os.makedirs(dest_folder_path)

#             # Extract the file name from the source file path
#             file_name = os.path.basename(src_file_path)
#             # Construct the destination file path
#             dest_file_path = os.path.join(dest_folder_path, file_name)

#             # Move the file
#             shutil.move(src_file_path, dest_file_path)
#             des_result+=dest_file_path
#             logging.info(f"Moved file to the destination folder _ {des_result.split(' ')}")
#         return des_result
#     except Exception as e:
#         logging.error("Couldn't move file to the destination folder _ {e}")