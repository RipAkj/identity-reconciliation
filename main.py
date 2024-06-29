
# from database.create_tables import create_tables
from fastapi import FastAPI,Depends,HTTPException,Query
from typing import Optional,Dict
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.types import Json
from src.database.db_support import get_db
from src.contact.router.contact_router import contact_router
from src.database.create_tables import create_tables


SECRET_KEY = "c2c78544f5fafc0673f1d2631c755571c11452d16dedf209060575b9d77ac82a"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTE = 30

class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI()
app.include_router(
    prefix=f"",
    router=contact_router,
    tags=["contact"],
    dependencies=[Depends(get_db)],
)
# create_tables()
