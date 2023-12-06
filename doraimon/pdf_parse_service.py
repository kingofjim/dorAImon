import requests

class PDFParseService:
    def __init__(self):
        pass

    def get_pdf_content_text(self, filepath):
        endpoint = 'http://20.104.173.107:5001'

        headers = {
            # 'Content-Type': 'multipart/form-data',
        }

        files = {
            'file': open(filepath, 'rb'),
        }

        url = f'{endpoint}/upload'

        try:
            response = requests.post(
                url,
                headers=headers,
                files=files,
            )
        except Exception as e:
            print(e)
        
        return response
