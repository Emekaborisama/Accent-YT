import requests

def fetch_voice_data():
    url = "https://api.elevenlabs.io/v1/voices"
    
    response = requests.get(url)
    result = response.json()

    result_id = [
        {k: v for k, v in voice.items() if k in ['voice_id', 'labels']}
        for voice in result['voices']
    ]

    return result_id

