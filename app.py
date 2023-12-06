import json
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from doraimon import azure_openai_service
from doraimon import azure_openai_whisper_service
from doraimon import prompt_solution_service
from doraimon import pdf_parse_service
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

openai_service = azure_openai_service.AzureOpenAIService()
openai_whisper_service = azure_openai_whisper_service.AzureOpenAIWhisperService()
pdf_parse_service = pdf_parse_service.PDFParseService()
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
    json_data = json.loads(data.text)

    messages = json_data['text'].split(".")
    # messages = ["Hello, my name is Bob and I am good at python", "Hi nice to meet you, python master"]

    prompt = pmptSvc.generate_further_question_prompt(messages)
    aiResult = openai_service.chat(prompt)

    messages.append(aiResult.content)

    return messages


@app.route('/cv_summary', methods=['POST'])
def cv_summary_post():
    files = request.files.getlist("file")
    cv = files[0]
    jd = files[1]

    cv.save(os.path.join('data', cv.filename))
    jd.save(os.path.join('data', jd.filename))

    cv_filepath = os.path.join('data', cv.filename)
    jd_filepath = os.path.join('data', jd.filename)

    cv_content = pdf_parse_service.get_pdf_content_text(cv_filepath)
    jd_content = pdf_parse_service.get_pdf_content_text(jd_filepath)
    print(cv_content.text)
    print(jd_content.text)
    
    cv_summary_prompt = pmptSvc.generate_cv_summary_prompt('soft_engineer', cv_content.text)
    cv_prompt_response = openai_service.chat(cv_summary_prompt)
    
    job_fit_prompt = pmptSvc.generate_job_fit_analysis_prompt(jd_content.text, cv_prompt_response.content)
    job_fit_prompt_response = openai_service.chat(job_fit_prompt)

    print(job_fit_prompt_response.content)
    return render_template('cv_summary.html', content=job_fit_prompt_response.content)

@app.route('/job_fit', methods=['GET'])
def job_fit():
    return render_template('job_fit.html')


if __name__ == ('__main__'):
    app.run(debug=True, host="0.0.0.0", ssl_context=('/cert/mycert.crt', '/cert/mykey.key'))
    # app.run(debug=True, host="0.0.0.0")
