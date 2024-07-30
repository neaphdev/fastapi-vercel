from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template

app = FastAPI()
current_dir = Path(__file__).parent


@app.get("/")
async def root(request: Request):
    print(request.headers)
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


@app.post("/a")
async def a(request: Request):

    return {"message": "the method was POST"}


@app.put("/b")
async def b(request: Request):

    return {"message": "the method was PUT"}


def get_app():
    return app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
