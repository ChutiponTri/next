from typing import Annotated
from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
my_token = os.getenv("API_TOKEN")
my_x_token = os.getenv("API_HEADER")

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != my_x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != my_token:
        raise HTTPException(status_code=400, detail="No Jessica token provided")