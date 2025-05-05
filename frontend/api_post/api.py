import requests

# Function to GET API Requests
def get_requests(endpoint=None):
    try:
        params = {
            "token": "{\p.,~GXK^<x"
        }
        headers = {
            "x-token": "zxeu-uzjnjy-vglrs"
        }
        # url = "http://172.20.10.3:8305/%s" % (endpoint or "")
        url = "http://localhost:8305/%s" % (endpoint or "")
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": response.status_code, "message": response.text}
    except Exception as E:
        print("GET Error :", E)

# Function to POST API Requests
def post_requests(endpoint=None, data=None):
    try:
        params = {
            "token": "{\p.,~GXK^<x"
        }
        headers = {
            "x-token": "zxeu-uzjnjy-vglrs"
        }
        # url = "http://172.20.10.3:8305/%s" % (endpoint or "")
        url = "http://localhost:8305/%s" % (endpoint or "")
        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            return response.json()
        else: 
            return {"status": response.status_code, "message": response.text}
    except Exception as E:
        print("POST Error :", E)

def preprocess_name(name:str, surname:str):
    return (name[0].upper() + name[1:].lower()).strip(), (surname[0].upper() + surname[1:].lower()).strip()
