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
