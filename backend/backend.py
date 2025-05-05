from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector as mysql
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

# Function to Initialize Database
def create_database():
    conn = mysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    cursor = conn.cursor()
    # query = "CREATE DATABASE IF NOT EXISTS %s"
    # c.execute(query, (eval(os.getenv("DATABASE")),))
    query = "CREATE DATABASE IF NOT EXISTS " + os.getenv("DATABASE")
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Get Database Connection
def get_db_connection():
    conn = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    return conn

# Function to Initialize Customer Table
def create_customers_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS customers (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        gender VARCHAR(16) NOT NULL,
        weight DECIMAL(11,7) NOT NULL,
        height DECIMAL(11,7) NOT NULL,
        disease VARCHAR(255) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to GET root
@app.get("/")
def hello_world():
    return {"Hello": "World"}

# BaseModel For Registration
class Register(BaseModel):
    name: str
    surname: str
    gender: str
    weight: float
    height: float
    disease: str

# Function to GET User
@app.get("/customers")
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM customers"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"Users": data}

# Function to POST Register
@app.post("/register")
def register(user:Register):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT name, surname FROM customers"
    cursor.execute(query)
    data = cursor.fetchall()
    if data:
        return {"Status": "User's Already Exists"}
    else:
        query = "INSERT INTO customers (name, surname, gender, weight, height, disease) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user.name, user.surname, user.gender, user.weight, user.height, user.disease))
        conn.commit()
        conn.close()
        return {"Status": "Inserted Successfully"}
    
# Function to Create Video Table
def create_video_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"""CREATE TABLE IF NOT EXISTS video (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        video VARCHAR(255) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Create AI Table
def create_ai_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f""" CREATE TABLE IF NOT EXISTS ai (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        bedsore VARCHAR(32) NOT NULL,
        hospital VARCHAR(96) NOT NULL,
        wound VARCHAR(96) NOT NULL,
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()
    
# Function to Create Health Monitoring

# BaseModel For Video History
class VideoHistory(BaseModel):
    username: str
    video: str

# Function to POST Video Session History
@app.post("/video/history")
def video_history(history:VideoHistory):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"INSERT INTO video (video) VALUES (%s)"
    cursor.execute(query, (history.video,))
    conn.commit()
    conn.close()
    return {"Status": "Inserted Successfully"}

# Function to Get Tata
@app.get("/tata")
def hello_tata():
    return {"Hello": "Tata"}

# Function to GET Teacher
@app.get("/teacher/{name}")
def hello_teacher(name):
    return {"Hello": "Teacher %s" % name}

# BaseModel For Sample Input
class Name(BaseModel):
    name: str
    age: int

@app.post("/input")
def input(name:str):
    return name

create_database()
create_customers_table()