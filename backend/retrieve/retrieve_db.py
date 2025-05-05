from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, date
from ..dependencies import get_token_header
from ..db_connection import get_db_connection

router = APIRouter(
    prefix="/retrieve",
    tags=["retrieve"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# Function to GET ALL Customers
@router.get("/customers")
async def customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM customers"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Specific Customer
@router.get("/customers/{name}/{surname}")
async def customer(name, surname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM customers WHERE name = %s AND surname = %s"
    cursor.execute(query, (name, surname))
    data = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET AI Prediction Result
@router.get("/ai/{name}/{surname}/{mode}/{day}")
async def ai_pred(name, surname, mode, day):
    conn = get_db_connection()
    cursor = conn.cursor()
    day = date.fromisoformat(day)
    if mode == "day":
        query = """
            SELECT 
                timestamp, bedsore_grade, suggestion, hospital, wound_type
            FROM 
                ai
            WHERE
                name = %s AND surname = %s AND DATE(timestamp) = %s
            ORDER BY
                timestamp ASC
        """
        cursor.execute(query, (name, surname, day))
    elif mode == "month":
        query = """
            SELECT 
                timestamp, bedsore_grade, suggestion, hospital, wound_type
            FROM 
                ai
            WHERE
                name = %s AND surname = %s AND MONTH(timestamp) = %s AND YEAR(timestamp) = %s
            ORDER BY
                timestamp ASC
        """
        cursor.execute(query, (name, surname, day.month, day.year))
    elif mode == "year":
        query = """
            SELECT 
                timestamp, bedsore_grade, suggestion, hospital, wound_type
            FROM 
                ai
            WHERE
                name = %s AND surname = %s AND YEAR(timestamp) = %s
            ORDER BY
                timestamp ASC
        """
        cursor.execute(query, (name, surname, day.year))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Appointment Date
@router.get("/appointment/{name}/{surname}")
async def appointment(name, surname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM appointment WHERE name = %s AND surname = %s ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(query, (name, surname))
    data = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Feedback 
@router.get("/feedback/{name}/{surname}")
async def feedback(name, surname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT timestamp, doctor_name, doctor_surname, descr 
        FROM feedback 
        WHERE name = %s AND surname = %s
        ORDER BY timestamp DESC LIMIT 7
    """
    cursor.execute(query, (name, surname))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Health Montoring
@router.get("/health/{name}/{surname}")
async def health(name, surname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT
            timestamp, evaluate_score, descr
        FROM
            health
        WHERE 
            name = %s AND surname = %s AND (
                timestamp BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
            )
    """
    cursor.execute(query, (name, surname))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Video History
@router.get("/video/{name}/{surname}")
async def video(name, surname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT timestamp, video FROM video WHERE name = %s AND surname = %s ORDER BY timestamp DESC LIMIT 10"
    cursor.execute(query, (name, surname))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Check-List
@router.get("/check/list/{name}/{surname}")
async def update_check_list(name, surname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT tasks FROM checklist WHERE name = %s AND surname = %s"
    cursor.execute(query, (name, surname))
    data = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"result": data}

# Function to GET Test
@router.get("/test")
async def test(name:str="Ton", age:int=20):
    return {"name": name, "age": age}
