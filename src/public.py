import importlib
import json
import logging
import os

from fastapi import APIRouter
from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse

import src
from src.commons import settings, headers

router = APIRouter()


@router.get('/linkset/{number}/json')
def get_links(number: str):
    try:
        with open(os.path.join(settings.RESOURCES_PATH, f'{number}.json')) as f:
            data = json.load(f)
    except:
        raise HTTPException(status_code=404, detail=f'linkset "{number}" not found')

    return data


@router.head('/page/{number}')
async def get_page(number: int):
    return JSONResponse(status_code=status.HTTP_200_OK, content=str(number), headers=headers(str(number)))

