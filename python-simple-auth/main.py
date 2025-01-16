from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/public", response_class=HTMLResponse, include_in_schema=False)
async def public(request: Request):
    return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'first_name': 'Mr.',
                'last_name': 'Anonymous'
                })

@app.get("/behind_proxy", response_class=HTMLResponse, include_in_schema=False)
async def behind_proxy(request: Request):

    return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'first_name': 'Dude'
                })

