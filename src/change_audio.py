import requests
import json

class SpeechToSpeechConverter:
    CHUNK_SIZE = 1024  # Size of chunks to read/write at a time

    def __init__(self, api_key, voice_id):
        self.api_key = api_key
        self.voice_id = voice_id
        self.sts_url = f"https://api.elevenlabs.io/v1/speech-to-speech/{self.voice_id}/stream"
        self.headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        self.data = {
            "model_id": "eleven_english_sts_v2",
            "voice_settings": json.dumps({
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            })
        }

    def convert_speech(self, input_file_path:str, output_file_path:str):
        files = {"audio": open(input_file_path, "rb")}
        response = requests.post(self.sts_url, headers=self.headers, data=self.data, files=files, stream=True)
        
        if response.ok:
            self._save_audio_stream(response, output_file_path)
            return ("Audio stream saved successfully.")
        else:
            return (response.text)

    def _save_audio_stream(self, response, output_file_path):
        with open(output_file_path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                output_file.write(chunk)
