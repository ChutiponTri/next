import requests

url = "http://127.0.0.1:8305/predict/"
path = "D:/Practice Housepital Back/dataset/pressureV1/test/Stage3AN_5_JPG_jpg.rf.71c5cdd2c66a388439cb6499c6ff1dc8.jpg"
headers = {
    "x-token": "zxeu-uzjnjy-vglrs"
}
params = {
    "token": "{\p.,~GXK^<x"
}

resp = requests.post(url, headers=headers, params=params, files={"file": open(path, "rb")})
if resp.status_code == 200:
    print(resp.json())
else:
    print(resp.status_code, resp.text)