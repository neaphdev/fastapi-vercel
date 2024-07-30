from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Template

app = FastAPI()
current_dir = Path(__file__).parent


@app.get("/")
async def root(request: Request):
    template_path = current_dir / "templates" / "index.html"
    with open(template_path, "r") as file:
        template_content = file.read()
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
