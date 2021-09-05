from pydantic import BaseModel


class Data(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
