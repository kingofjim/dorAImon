import os
import requests
from dotenv import load_dotenv


class AzureOpenAIWhisperService:
    def __init__(self):
        load_dotenv()

    def get_transcriptions(filepath):
        endpoint = os.getenv("AZURE_W_OPENAI_ENDPOINT")
        key = os.getenv("AZURE_W_OPENAI_KEY")
        headers = {
            'api-key': key,
            # requests won't add a boundary if this header is set when you pass files=
            # 'Content-Type': 'multipart/form-data',
        }

        params = {
            'api-version': '2023-09-01-preview',
        }

        files = {
            'file': open(filepath, 'rb'),
        }

        url = f'{endpoint}/openai/deployments/whisper001/audio/transcriptions'

        response = requests.post(
            url,
            params=params,
            headers=headers,
            files=files,
        )

        return response
