import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from doraimon import azure_openai_service
from doraimon import azure_openai_whisper_service
from doraimon import prompt_solution_service


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

openai_service = azure_openai_service.AzureOpenAIService()
openai_whisper_service = azure_openai_whisper_service.AzureOpenAIWhisperService()
pmptSvc = prompt_solution_service.PromptSolutionService()

@app.route('/')
def index():
    message = request.args['message']
    response = openai_service.chat(message)
    return render_template('index.html', response=response, history=openai_service.history)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join('data', file.filename))
    filepath = os.path.join('data', file.filename)
    
    data = openai_whisper_service.get_transcriptions(filepath)
    messages = data.text.split(".")
    # messages = ["Hello, my name is Bob and I am good at python", "Hi nice to meet you, python master"]

    prompt = pmptSvc.generate_further_question_prompt(messages)
    aiResult = openai_service.chat(prompt)
    
    messages.append(aiResult.content)

    return messages

if __name__ == ('__main__'):
    app.run(debug=True, host="0.0.0.0", ssl_context=('/cert/mycert.crt', '/cert/mykey.key'))
