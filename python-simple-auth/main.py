from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/public", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'first_name': 'Dude'
                })

