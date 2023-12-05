from flask import Flask, render_template, request
from dotenv import load_dotenv
from doraimon import azure_openai_service
from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage
from flask.helpers import send_file
from datetime import datetime
from io import BytesIO
import fitz
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

openai_service = azure_openai_service.AzureOpenAIService()


@app.route('/')
def index():
    message = request.args['message']
    response = openai_service.chat(message)
    return render_template('index.html', response=response, history=openai_service.history)


@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    return render_template('upload_resume.html')

def convert_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()

    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

    return text


def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})


upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@api.route('/upload')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        timestamp = datetime.timestamp(datetime.now())
        timestamp_string = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if uploaded_file:
            upload_folder = 'uploads'

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            file_path = os.path.join(upload_folder, uploaded_file.filename)
            uploaded_file.save(file_path)
            pdf_text = convert_text_from_pdf(file_path)
            uploaded_file.close()

            blob_name = uploaded_file.filename
            blob_client = container_client.get_blob_client(blob_name)
            with open(file=os.path.join(upload_folder, blob_name), mode="rb") as data:
                blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)

            return {'pdf_text': pdf_text}, 201

        return {'error': 'No file provided'}, 400


@api.route('/download/<string:blob_name>')
class DownloadBlob(Resource):
    def get(self, blob_name):
        try:
            # Get the blob client for the specified blob name
            file_name = blob_name + '.pdf'
            blob_client = container_client.get_blob_client(file_name)

            # Download blob data
            blob_data = blob_client.download_blob().readall()

            # Create an in-memory file-like object for sending the data
            in_memory_file = BytesIO(blob_data)

            # Send the file for download
            return send_file(
                in_memory_file,
                download_name=file_name,
                as_attachment=True,
                mimetype='application/pdf'  # Specify the MIME type
            )
        except Exception as e:
            return {'error': f'Error downloading blob: {str(e)}'}, 500


if __name__ == ('__main__'):
    app.run(debug=True, host="0.0.0.0")
