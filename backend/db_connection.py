import mysql.connector as mysql
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Function to Initialize Database
def create_database():
    conn = mysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS " + os.getenv("DB_NAME")
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Get Database Connection
def get_db_connection():
    conn = mysql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_ROOT"),
        password=os.getenv("DB_PASSWORD")
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
        disease VARCHAR(255) NOT NULL,
        birth DATE NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Create Video Table
def create_video_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS video (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        video VARCHAR(255) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Create AI Table
def create_ai_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS ai (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        bedsore_grade VARCHAR(32) NOT NULL,
        suggestion VARCHAR(255),
        hospital VARCHAR(96) NOT NULL,
        wound_type VARCHAR(96) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()
    
# Function to Create Health Monitoring
def create_health_monitor():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS health (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        evaluate_score DECIMAL(11,7) NOT NULL,
        descr VARCHAR(48) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Create Appointment Table
def create_appointment_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS appointment (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        date DATETIME NOT NULL,
        place VARCHAR(96) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Create Doctor Feedback Table
def create_doctor_feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS feedback (
        timestamp DATETIME PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        doctor_name VARCHAR(255) NOT NULL,
        doctor_surname VARCHAR(255) NOT NULL,
        descr VARCHAR(255) NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

# Function to Create Check List
def create_check():
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

# Function to Insert Check List
def insert_check_list(name, surname, tasks):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO checklist (name, surname, tasks) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            tasks = VALUES(tasks)
    """
    cursor.execute(query, (name, surname, json.dumps(tasks)))
    conn.commit()
    conn.close()
    return {"status": "CheckList Successfully"}

# Function to Create ALL Tables
def create_all():
    create_database()
    create_customers_table()
    create_ai_table()
    create_appointment_table()
    create_health_monitor()
    create_video_table()
    create_doctor_feedback()
    create_check()