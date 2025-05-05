# pip install streamlit-autorefresh
import streamlit as st
from datetime import datetime
import json
from api_request import get_root, post_requests, get_checklist

class Admin():
    def __init__(self):
        self.header()
        self.sidebar()
        self.welcome()
        self.display_data()
        self.post_status()

    # Function to Initialize Header   
    def header(self):
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

        # Set Page Header
        st.header("Housepital :blue[Care]", divider="rainbow")

    # Function to Initialize Sidebar
    def sidebar(self):
        pass

    # Function to Display Welcome Message
    def welcome(self):
        # Initialize WELCOME Session State
        if "WELCOME" not in st.session_state:
            st.session_state.WELCOME = get_root()
            print(st.session_state.WELCOME)

        # Display Welcome Message
        st.write(st.session_state.WELCOME["message"])
    
    # Function to Display Query Data
    def display_data(self):
        pass

    # Function to Display Post Status
    def post_status(self):
        # Display POST Status From Session State
        if "POST" in st.session_state:
            if "message" in st.session_state.POST.keys():
                if "Not" in st.session_state.POST["message"]:
                    st.subheader(st.session_state.POST["message"])

class Respond():
    def __init__(self):
        self.header()
        self.sidebar()
        self.welcome()
        self.display_data()
        self.post_status()

    # Function to Initialize Header   
    def header(self):
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
        
        # Set Page Header
        st.header("Housepital :blue[Care]", divider="rainbow")

    # Function to Initialize Sidebar
    def sidebar(self):
        pass

    # Function to Display Welcome Message
    def welcome(self):
        # Initialize WELCOME Session State
        if "WELCOME" not in st.session_state:
            st.session_state.WELCOME = get_root()
            print(st.session_state.WELCOME)

        if "tasks" not in st.session_state:
            name, surname = st.session_state.current_user.split(" ")
            st.session_state.tasks = get_checklist(name, surname)

    # Function to Get Current Time
    def get_time_of_day(self):
        # Get the current hour
        current_hour = datetime.now().hour
        
        # Define time periods based on hour ranges
        if 5 <= current_hour < 9:
            return "ช่วงเช้า"
        elif 9 <= current_hour < 12:
            return "ก่อนเที่ยง"
        elif 12 <= current_hour < 16:
            return "ช่วงกลางวัน"
        elif 16 <= current_hour < 19:
            return "ช่วงเย็น"
        else:
            return "ตอนค่ำ"
    
    # Function to Display Query Data
    def display_data(self):
        # st.video("https://youtu.be/_Ra0OAvFdBE?si=3YdiOlXHRDuh73In")
        # st.video("http://localhost:8305/video/get?token={\p.,~GXK^%3Cx")
        # st.header("My name's %s" % st.session_state.current_user)

        period = self.get_time_of_day()
        st.subheader(f"งานดูแลผู้ป่วย{period}")

        # tasks = ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "พาไปอาบน้ำ", "ตรวจแผลกดทับ", "เปลี่ยนผ้าอ้อม", "อาหารมื้อแรกของวัน", "ยาก่อน/หลังอาหาร"]
        tasks = json.loads(st.session_state.tasks["result"][0])[period]
        task_dict = {}
        for task in tasks:
            task_dict[task] = st.checkbox(task)
            if task == "วัดอัตราการเต้นของหัวใจ":
                if task_dict[task]:
                    hr = st.number_input("อัตราการเต้นของหัวใจ", min_value=0, value=None, placeholder="กรุณาใส่ข้อมูลอัตราการเต้นของหัวใจ (BPM) เช่น 60, 80, 95", key="hr")
            elif task == "วัดความดันเลือด":
                if task_dict[task]:
                    pressure = st.number_input("วัดความดันเลือด", min_value=0, value=None, placeholder="กรุณาใส่ข้อมูลความดันเลือด (mmHg) เช่น 150/90, 140/90", key="pressure")
            elif task == "วัดระดับน้ำตาลในเลือด":
                if task_dict[task]:
                    sugar = st.number_input("วัดระดับน้ำตาลในเลือด", min_value=0, value=None, placeholder="กรุณาใส่ข้อมูลอัตราการเต้นของหัวใจ (mg/dL) เช่น 70, 80, 100", key="sugar")
            elif task == "ตรวจแผลกดทับ":
                if task_dict[task]:
                    camera = st.page_link("web/ai.py", label="AI Camera", icon="📷")
        if st.button("บันทึก"):
            st.success("สำเร็จ")

    # Function to Display Post Status
    def post_status(self):
        try:
            # Display POST Status From Session State
            if "POST" in st.session_state:
                if "message" in st.session_state.POST.keys():
                    if "Not" in st.session_state.POST["message"]:
                        st.subheader(st.session_state.POST["message"])
            # print([i.name for i in Enumerate()])
        except Exception as e:
            st.write(e)

if st.session_state.role == "Admin":
    admin = Admin()
elif st.session_state.role == "Responder":
    respond = Respond()

