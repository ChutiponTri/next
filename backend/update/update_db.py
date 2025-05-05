from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List
import random
import json
from ..dependencies import get_token_header
from ..db_connection import get_db_connection, insert_check_list

router = APIRouter(
    prefix="/update",
    tags=["update"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# BaseModel For Registration
class Register(BaseModel):
    name: str
    surname: str
    gender: str
    weight: float
    height: float
    disease: str
    birth: str

# Function to POST Register
@router.post("/register")
async def register(user:Register):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT name, surname FROM customers WHERE name=%s AND surname=%s"
    cursor.execute(query, (user.name, user.surname))
    data = cursor.fetchone()
    if data:
        return {"status": "User's Already Exists", "result": data}
    else:
        query = "INSERT INTO customers (name, surname, gender, weight, height, disease, birth) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user.name, user.surname, user.gender, user.weight, user.height, user.disease, user.birth))
        conn.commit()
        conn.close()
        task_list = [
            "วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด",
            "พาไปอาบน้ำ", "ตรวจแผลกดทับ", "เปลี่ยนผ้าอ้อม",
            "อาหารมื้อแรกของวัน", "ยาก่อน/หลังอาหาร"
        ]

        time_slots = ["ช่วงเช้า", "ก่อนเที่ยง", "ช่วงกลางวัน", "ช่วงเย็น", "ตอนค่ำ"]
        random.shuffle(task_list)

        tasks = {
            time_slots[i]: task_list[i*3:(i+1)*3]
            for i in range(len(time_slots))
        }
        insert_check_list(user.name, user.surname, tasks)
        return {"status": "Register Successfully"}

# BaseModel For Customer Modification
class Modification(BaseModel):
    id: int
    name: str
    surname: str
    gender: str
    weight: float
    height: float
    disease: str
    birth: str

# Function to POST Update Customer Data
@router.post("/customers/edit")
async def edit(user:Modification):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE customers SET name=%s, surname=%s, gender=%s, weight=%s, height=%s, disease=%s, birth=%s WHERE id=%s"
    try:
        cursor.execute(query, (user.name, user.surname, user.gender, user.weight, user.height, user.disease, user.birth, user.id))
    except Exception as e:
        return {"status": e}
    conn.commit()
    conn.close()
    return {"status": "Edit Successfully"}
    
# BaseModel For AI
class AI(BaseModel):
    name: str
    surname: str
    bedsore_grade: str
    suggestion: str
    hospital: str
    wound_type: str
    
# Function to POST AI
@router.post("/ai")
async def post_ai(data:AI):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO ai (name, surname, bedsore_grade, suggestion, hospital, wound_type) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (data.name, data.surname, data.bedsore_grade, data.suggestion, data.hospital, data.wound_type))
    conn.commit()
    conn.close()
    return {"status": "AI Successfully"}

# BaseModel For Appointment
class Appointment(BaseModel):
    name: str
    surname: str
    date: str
    place: str

# Function to POST Appointment
@router.post("/appointment")
async def post_appoint(data:Appointment):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO appointment (name, surname, date, place) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data.name, data.surname, data.date, data.place))
    conn.commit()
    conn.close()
    return {"status": "Appointment Successfully"}

# BaseModel For Doctor Feedback
class Feedback(BaseModel):
    name: str
    surname: str
    doctor_name: str
    doctor_surname: str
    descr: str

# Function to POST Feedback
@router.post("/feedback")
async def post_feedback(data:Feedback):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO feedback (name, surname, doctor_name, doctor_surname, descr) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (data.name, data.surname, data.doctor_name, data.doctor_surname, data.descr))
    conn.commit()
    conn.close()
    return {"status": "Feedback Successfully"}

# BaseModel For Health Evaluation
class HealthEvaluate(BaseModel):
    name: str
    surname: str
    evaluate_score: float
    descr: str

# Function to POST Health Evaluation
@router.post("/health")
async def post_health_eval(data:HealthEvaluate):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO health (name, surname, evaluate_score, descr) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data.name, data.surname, data.evaluate_score, data.descr))
    conn.commit()
    conn.close()
    return {"status": "Health Successfully"}

# BaseModel For Video History
class VideoHistory(BaseModel):
    name: str
    surname: str
    video: str

# Function to POST Video History
@router.post("/video")
async def post_video_hist(data:VideoHistory):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO video (name, surname, video) VALUES (%s, %s, %s)"
    cursor.execute(query, (data.name, data.surname, data.video))
    conn.commit()
    conn.close()
    return {"status": "Video Successfully"}

# Temporary Function to Create Check-List Table
@router.post("/check/list")
async def temp_create_check():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS checklist(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            tasks JSON NOT NULL,
            UNIQUE (name, surname)  -- Ensures the combination of name and surname is unique
        )"""
    cursor.execute(query)
    conn.commit()
    conn.close()


# Base Model For Check-List
class CheckList(BaseModel):
    name: str
    surname: str
    tasks: Dict[str, List[str]]

# Function to POST Upsert Check-List
@router.post("/check/list/upsert")
async def insert_check(data:CheckList):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO checklist (name, surname, tasks) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            tasks = VALUES(tasks)
    """
    cursor.execute(query, (data.name, data.surname, json.dumps(data.tasks)))
    conn.commit()
    conn.close()
    return {"status": "CheckList Successfully"}

