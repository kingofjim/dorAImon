import os
from dotenv import load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    AIMessagePromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ChatMessageHistory
from langchain.chat_models import AzureChatOpenAI


class AzureOpenAIService:
    def __init__(self):
        load_dotenv()

        self.chatbot = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_version="2023-07-01-preview",
            deployment_name="gpt-35-turbo-16k_canadaeast",
            openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
            openai_api_type="azure",
            temperature=0.7,
        )

    def chat(self, text):
        human_template = """{user_message}"""
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template)
        
        message = human_message_prompt.format_messages(user_message=text)
        
        response = self.chatbot(message)

        return response