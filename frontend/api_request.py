import streamlit as st
import requests
from dotenv import load_dotenv
import os

if "env" not in st.session_state:
    load_dotenv()
    st.session_state["env"] = True

# Function to GET API Requests
def get_requests(endpoint=None):
    try:
        params = {
            "token": os.getenv("API_TOKEN")
        }
        headers = {
            "x-token": os.getenv("API_HEADER")
        }
        # url = "http://172.20.10.3:8305/%s" % (endpoint or "")
        url = f"""http://{os.getenv("HOST")}:{os.getenv("PORT")}/{endpoint or ""}"""
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            st.session_state["GET"] = response.json()
            return response.json()
        else:
            st.session_state["GET"] = response.status_code
            return {"status": response.status_code, "message": response.text}
    except Exception as E:
        print("GET Error :", E)

# Function to POST API Requests
def post_requests(endpoint=None, data=None):
    try:
        params = {
            "token": os.getenv("API_TOKEN")
        }
        headers = {
            "x-token": os.getenv("API_HEADER")
        }
        url = f"""http://{os.getenv("HOST")}:{os.getenv("PORT")}/{endpoint or ""}"""
        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            st.session_state["POST"] = response.json()
            return response.json()
        else: 
            st.session_state["POST"] = {"status": response.status_code, "message": response.text}
            return {"status": response.status_code, "message": response.text}
    except Exception as E:
        print("POST Error :", E)

# Function to Preprocess Name Data
def preprocess_name(name:str, surname:str):
    return (name[0].upper() + name[1:].lower()).strip(), (surname[0].upper() + surname[1:].lower()).strip()

# Function to GET Root
def get_root():
    endpoint = "retrieve"
    return get_requests(endpoint)

# Function to GET AI Data
def get_ai(name, surname, mode, day):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/ai/%s/%s/%s/%s" % (name, surname, mode, day)
    return get_requests(endpoint)

# Function to GET ALL Customers
def get_all_customers():
    endpoint = "retrieve/customers"
    return get_requests(endpoint)

# Function to GET Appointment
def get_appointment(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/appointment/%s/%s" % (name, surname)
    return get_requests(endpoint)

# Function to GET Single Customer
def get_customer(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/customers/%s/%s" % (name, surname)
    return get_requests(endpoint)

# Function to GET Feedback Data
def get_feedback(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/feedback/%s/%s" % (name, surname)
    return get_requests(endpoint)

# Function to GET Health Monitor
def get_health(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/health/%s/%s" % (name, surname)
    return get_requests(endpoint)

# Function to GET Video History
def get_video(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/video/%s/%s" % (name, surname)
    return get_requests(endpoint)

# Function to GET Check-List
def get_checklist(name, surname):
    name, surname = preprocess_name(name, surname)
    endpoint = "retrieve/check/list/%s/%s" % (name, surname)
    return get_requests(endpoint)

# Function to POST Edit Customer Data
def post_edit(data):
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    endpoint = "update/customers/edit"
    return post_requests(endpoint, data)

# Function to POST AI Data
def post_ai(data):
    endpoint = "update/ai"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

# Function to POST Appointment
def post_appointment(data):
    endpoint = "update/appointment"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

# Function to POST Register
def post_register(data):
    endpoint = "update/register"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

# Function to POST Feedback
def post_feedback(data):
    endpoint = "update/feedback"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

# Function to POST Health Monitoring
def post_health(data):
    endpoint = "update/health"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

# Function to POST Video History
def post_video(data):
    endpoint = "update/video"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)

# Function to POST Upsert Check-List
def post_checklist(data):
    endpoint = "update/check/list/upsert"
    data["name"], data["surname"] = preprocess_name(data["name"], data["surname"])
    return post_requests(endpoint, data)