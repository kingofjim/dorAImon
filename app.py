import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from doraimon import azure_openai_service
from doraimon import azure_openai_whisper_service

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

openai_service = azure_openai_service.AzureOpenAIService()
openai_whisper_service = azure_openai_whisper_service.AzureOpenAIWhisperService()


@app.route('/')
def index():
    message = request.args['message']
    response = openai_service.chat(message)
    return render_template('index.html', response=response, history=openai_service.history)

def upload():
    file = request.files['file']
    file.save(os.path.join('data', file.filename))
    filepath = os.path.join('data', file.filename)
    
    return openai_whisper_service.get_transcriptions(filepath)

if __name__ == ('__main__'):
    app.run(debug=True, host="0.0.0.0")
