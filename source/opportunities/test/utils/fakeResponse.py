import os

from scrapy.http import Response, Request

def fake_response_from_file(file_name, url=None):
    

    if not url:
        url = "https://www.example.com"

    request = Request(url=url)
    if not file_name[0] == '/':
        response_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(response_dir, file_name)
    else:
        file_path = file_name
    
    file_content = None
    with open(file_path, 'r') as html_file:
        file_content = html_file.read()
    
    if file_content is None:
        raise RuntimeError("Couldn't read in file")
    
    response = Response(
        url=url,
        request=request,
        body=file_content
    )
    response.encoding = 'utf-8'
    return response
    