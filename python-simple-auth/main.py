from functools import cache

from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from jwt import PyJWKClient, decode

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/public", response_class=HTMLResponse, include_in_schema=False)
async def public(request: Request):
    return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'name': 'Anonymous'
                })

@cache
def get_signing_key(token: str) -> str:
    jwks_client = PyJWKClient(
            'https://login.microsoftonline.com/3b7e4170-8348-4aa4-bfae-06a3e1867469/discovery/v2.0/keys'
            )
    return jwks_client.get_signing_key_from_jwt(token).key
    

@app.get("/behind_proxy", response_class=HTMLResponse, include_in_schema=False)
async def behind_proxy(request: Request):
    print(request.headers)
    userinfo: dict  = {}
    try:
        id_token = request.headers.get('Authorization', default='').split(' ')[1]
        # This token has already been verified, but let's do it again to practice 
        # defense in depth
        signing_key = get_signing_key(id_token)
        userinfo = decode(
                id_token,
                signing_key,
                algorithms=["RS256"],
                audience='653c520a-0892-4d0d-bdd1-8ac295995037'
                )

    except Exception as e:
        return str(e)
    
    name = userinfo['name']

    return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={
                'name': name,
                'userinfo': userinfo
                })
