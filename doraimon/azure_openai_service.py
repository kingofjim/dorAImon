import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI


class AzureOpenAIService:
    def __init__(self):
        load_dotenv()

        self.chatbot = AzureChatOpenAI(
            openai_api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_version="2023-05-15",
            deployment_name="gpt-35-turbo_team1189",
            openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
            openai_api_type="azure",
        )
