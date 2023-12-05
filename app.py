from flask import Flask, render_template, request
from dotenv import load_dotenv
from doraimon import azure_openai_service

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

openai_service = azure_openai_service.AzureOpenAIService()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == ('__main__'):
    app.run()