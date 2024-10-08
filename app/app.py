from pathlib import Path
import requests

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
current_dir = Path(__file__).parent


@app.get("/")
async def root(request: Request):
    template_path = current_dir / "templates" / "index.html"
    with open(template_path, "r") as file:
        template_content = file.read()
    url = 'https://api.thecatapi.com/v1/images/0XYvRd7oD'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'YOUR_API_KEY'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("DATA:: ",data)
    else:
        print(f'Error: {response.status_code}')
    template = Template(template_content)
    content = template.render(
        request=request,
        message="Hello, World!",
        url_for=lambda name, **path_params: request.url_for(name, **path_params),
    )

    return HTMLResponse(content)


@app.put("/")
async def a(request: Request):
    # Get form data including file and method key
    form = await request.form()

    # Extract the file from the form data
    file = form.get("file")  # file should match the field name in the form
    method = form.get("method")  # method should match the field name in the form

    # Print headers, file, and method
    headers = dict(request.headers)
    print("Headers:", headers)

    # Extracting file content if it's available
    if file:
        file_content = await file.read()
        print("File content:", file_content.decode())  # Decoding from bytes to string

    print("Method:", method)

    return JSONResponse(content={"message": "the method was POST", "method": method})


@app.put("/b")
async def b(request: Request):

    return {"message": "the method was PUT"}


def get_app():
    return app


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
