import os

from fastapi import APIRouter
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import src

# get the current working directory
cur_working_dir = os.getcwd()
cur_parent_dir = os.path.abspath(os.path.join(cur_working_dir, os.pardir))
base_dir = os.getenv("BASE_DIR", default=cur_parent_dir)
router = APIRouter()
templates = Jinja2Templates(directory=f'{base_dir}/pages-templates')
router.mount('/static', StaticFiles(directory=f'{base_dir}/static'), name='static')


@router.get('/home')
def home(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request,  'vers': src.main.__version__})

@router.get('/status')
def home(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request,  'vers': src.main.__version__})
