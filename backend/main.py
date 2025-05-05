from fastapi import FastAPI, Depends
from datetime import datetime
from .dependencies import get_query_token, get_token_header
from .db_connection import create_all
from .update import update_db
from .retrieve import retrieve_db
from .prediction import prediction

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(update_db.router)
app.include_router(retrieve_db.router)
app.include_router(prediction.router)

# Function to GET root
@app.get("/retrieve")
def hello_world():
    return {"message": "Hello From Housepital", "timestamp": datetime.now()}

create_all()