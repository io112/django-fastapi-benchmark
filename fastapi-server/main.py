from typing import Optional, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from models import SessionLocal

app = FastAPI()

from pydantic import BaseModel


class EntityBase(BaseModel):
    id: Optional[int]
    field1: int
    field2: str

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/simple/get')
def get():
    return {"message": "This is an async class based view."}


@app.post('/simple/get')
def post(req: str):
    return req


@app.get('/db/get/{f1}', response_model=List[EntityBase])
def db_read(f1: int, db: Session = Depends(get_db)):
    res = db.query(models.Entity).where(models.Entity.field1 == f1).all()
    return res


@app.post('/db/post', response_model=EntityBase)
def db_read(e: EntityBase, db: Session = Depends(get_db)):
    res = models.Entity(**e.dict())
    db.add(res)
    db.commit()
    return res
