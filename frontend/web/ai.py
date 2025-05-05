import streamlit as st
from api_request import post_requests, get_requests
from PIL import Image
import requests
from dotenv import load_dotenv
import json
import io
import os

if "env" not in st.session_state:
    load_dotenv()
    st.session_state["env"] = True

if "current_user" in st.session_state:
    fullname = st.session_state.current_user
    st.html("""
        <style>
            .myHeader {
                text-align: right;
                font-size: 1.5em;
            }
        </style>
        <div>
            <p class="myHeader">User : %s</p>
        </div>""" % (fullname)
    )

suggestion = {
    1: "ควรหลีกเลี่ยงการกดทับและรักษาความชุ่มชื้นของผิวหนังโดยการเปลี่ยนท่าทุกๆ 2 ชั่วโมง",
    2: "ควรรักษาความสะอาดแผล ใช้ผลิตภัณฑ์ฆ่าเชื้อ และเปลี่ยนท่าทุกๆ 1-2 ชั่วโมงเพื่อป้องกันการติดเชื้อ",
    3: "ควรไปพบแพทย์เพื่อรับการรักษาแผลที่ลึกและใช้ผ้าพันแผลที่เหมาะสมในการป้องกันการติดเชื้อ",
    4: "ควรรักษาแผลในโรงพยาบาลโดยการดูแลจากแพทย์และพยาบาลเพื่อป้องกันการติดเชื้อและลุกลามของแผล"
}

st.header("ระบบ AI ตรวจจับบาดแผลและปัสสาวะ", divider="rainbow")

def capture_image():
    img_file = st.camera_input("กล้องถ่ายรูป")

    if img_file is not None:
        # Open Image as PIL object
        img = Image.open(img_file)

        # Convert to RGB if needed
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Display the captured image
        # st.image(img, "ภาพถ่าย")

        # Convert the Image to a supported format in memory
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")   # Save as PNG
        img_bytes.seek(0)                   # Move to the start of the file-like object

        return img_bytes

    return None

def upload_image():
    file = st.file_uploader("เลือกรูปภาพ", type=["png", "jpg", "jpeg"])
    if file is not None:
        # Read the uploaded file as bytes
        img_bytes = file.read()

        # Use PIL to open the image from bytes
        img = Image.open(io.BytesIO(img_bytes))

        # Display the uploaded image in Streamlit
        st.image(img, "รูปภาพที่เลือก")

        return img_bytes
     
    return None

def get_prediction(img_bytes):
    params = {
            "token": os.getenv("API_TOKEN")
    }
    headers = {
        "x-token": os.getenv("API_HEADER")
    }
    url = f"""http://{os.getenv("HOST")}:8305/predict/"""
    response = requests.post(
        url=url,
        headers=headers,
        params=params,
        files={"file": ("image.jpg", img_bytes, "image/jpeg")}  # Ensure JPEG format
    )
    return response

upload_img = upload_image()
if upload_img is not None:
    # Button to send the request
    if st.button("Analyze Image"):
        response = get_prediction(upload_img)
        if response.status_code == 200:
            print(response.text)
            data = json.loads(response.text)
            if "pred_labels" in data.keys():
                level = data["pred_labels"]
                st.html("""
                    <div>
                        <u style="font-size: 2em; font-weight: bold;">Bedsore Grade %d</u>
                        <p style="font-size: 1.2em; font-weight: bold;">%s</p>
                    </div>
                """ % (level, suggestion[level]))
                # st.subheader("Bedsore Grade %d" % level)
                # st.subheader(suggestion[level])
        else:
            st.error(f"Error: {response.status_code}")
            st.write(response.text)
else:
    img_bytes = capture_image()
    if img_bytes is not None:
        # Button to send the request
        if st.button("Analyze Image"):
            response = get_prediction(img_bytes)
            if response.status_code == 200:
                print(response.text)
                data = json.loads(response.text)
                if "pred_labels" in data.keys():
                    level = data["pred_labels"]
                    st.html("""
                        <div>
                            <u style="font-size: 2em; font-weight: bold;">Bedsore Grade %d</u>
                            <p style="font-size: 1.2em; font-weight: bold;">%s</p>
                        </div>
                    """ % (level, suggestion[level]))
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)



