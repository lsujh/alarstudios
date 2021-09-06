import asyncio
import json

import aiofiles
from fastapi import File
from sqlalchemy.orm import Session

from app.models.data import Data


def add_data(content: File, db: Session) -> None:
    try:
        datas = []
        for i in content:
            datas.append(Data(**i))
        db.add_all(datas)
        db.commit()
    except:
        pass


async def read_file(file_name):
    async with aiofiles.open(file_name, mode='r') as f:
        content = await f.read()
        return json.loads(content)


def list_merge(_contents) -> list:
    contents = []
    for content in _contents:
        contents.extend(content)
    return sorted(contents, key=lambda content: content['id'])


def read_files_async(file_names: list) -> list:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        contents = loop.run_until_complete(asyncio.wait_for(
            asyncio.gather(*[read_file(file_name) for file_name in file_names],
                           return_exceptions=True), timeout=2.0))
        return list_merge(contents)
    except asyncio.TimeoutError:
        pass
