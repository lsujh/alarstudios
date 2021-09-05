import asyncio
import json

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.templating import Jinja2Templates

from app.constants import BASE_PATH
from app.crud.data import add_data
from app.db.session import get_db

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.post("/datas/")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        content = json.loads(content)
        add_data(content, db)
    except:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Bad request",
        )
    return content


@router.get("/datas/")
async def list_data(request: Request, db: Session = Depends(get_db)):
    sql = text("SELECT id, name FROM datas ORDER BY id ASC")
    datas = db.execute(sql)
    return templates.TemplateResponse("data/list-data.html", {"request": request, "datas": datas})


@router.post("/upload-data/")
async def upload_data(request: Request, db: Session = Depends(get_db)):
    files = ['/usr/src/source_1.json', '/usr/src/source_2.json', '/usr/src/source_3.json']
    for file in files:
        async with aiofiles.open(file, 'r') as f:
            content = await f.read()
        try:
            await asyncio.wait_for(aiofiles.open(file, 'r'), timeout=2)
            content = json.loads(content)
            add_data(content, db)
        except asyncio.TimeoutError:
            continue

    return RedirectResponse(request.url_for('list_data'), status_code=302)
