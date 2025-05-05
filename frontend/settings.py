import streamlit as st
from datetime import date
import json
from api_request import get_checklist, post_checklist, post_edit

class Setting():
    def __init__(self):
        self.header()
        self.sidebar()
        self.query()
        self.edit_form()

    # Function to Initialize Header
    def header(self):
        if "current_user" in st.session_state:
            self.fullname = st.session_state.current_user
            st.html("""
                <style>
                    .myHeader {
                        text-align: right;
                        font-size: 1.5em;
                    }
                </style>
                <div>
                    <p class="myHeader">User : %s</p>
                </div>""" % (self.fullname)
            )
        # Create Header Content
        st.header("การตั้งค่า", divider="rainbow")

    # Function to Initialize Sidebar
    def sidebar(self):
        pass

    # Function to Query for Check-List
    def query(self):
        if "SETTING" not in st.session_state:
            self.name, self.surname = self.fullname.split(" ")

            st.session_state.SETTING = get_checklist(self.name, self.surname)

        if "tasks" not in st.session_state:
            name, surname = st.session_state.current_user.split(" ")
            st.session_state.tasks = get_checklist(name, surname)

    # Function to Initialize Edit Form
    def edit_form(self):
        print(st.session_state.SETTING)
        data = json.loads(st.session_state.SETTING["result"][0])
        tabs = ["ช่วงเช้า", "ก่อนเที่ยง", "ช่วงกลางวัน", "ช่วงเย็น", "ตอนค่ำ"]
        tasks = ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "พาไปอาบน้ำ", "ตรวจแผลกดทับ", "เปลี่ยนผ้าอ้อม", "อาหารมื้อแรกของวัน", "ยาก่อน/หลังอาหาร"]
        morning, late, afternoon, evening, night = st.tabs(tabs)
        with morning:
            morning_tasks = {}
            for task in tasks:
                morning_tasks[task] = st.toggle(task, value=True if task in data["ช่วงเช้า"] else False, key=f"morning_{task}")
        with late:
            # st.multiselect("ก่อนเที่ยง", tasks)
            late_tasks = {}
            for task in tasks:
                late_tasks[task] = st.toggle(task, value=True if task in data["ก่อนเที่ยง"] else False, key=f"late_{task}")
        with afternoon:
            afternoon_tasks = {}
            for task in tasks:
                afternoon_tasks[task] = st.toggle(task, value=True if task in data["ช่วงกลางวัน"] else False, key=f"noon_{task}")
        with evening:
            evening_tasks = {}
            for task in tasks:
                evening_tasks[task] = st.toggle(task, value=True if task in data["ช่วงเย็น"] else False, key=f"evening_{task}")
        with night:
            night_tasks = {}
            for task in tasks:
                night_tasks[task] = st.toggle(task, value=True if task in data["ตอนค่ำ"] else False, key=f"night_{task}")

        if st.button("บันทึกข้อมูล"):
            all_dict = [morning_tasks, late_tasks, afternoon_tasks, evening_tasks, night_tasks]
            all_tasks = {tabs[i]: [task for task in tasks if timing[task]] for i, timing in enumerate(all_dict)}
            # st.write(all_tasks)

            self.on_editor(self.name, self.surname, all_tasks)

        if type(data) == list and len(data) > 5:
            print(data)

            form = st.form("Account Editor")
            name_surname = form.columns(2)
            name = name_surname[0].text_input("ชื่อ", placeholder="กรอกชื่อ", value=data[1])
            surname = name_surname[1].text_input("นามสกุล", placeholder="กรอกนามสกุล", value=data[2])

            gender_birth = form.columns(3)
            gender = gender_birth[0].selectbox("เพศ", ["ชาย", "หญิง", "ไม่ระบุ"], index=0 if data[3] in ["ชาย", "Male"] else 1)
            birth = gender_birth[1].date_input("วันเดือนปีเกิด", min_value=date(1900, 1, 1), value=date.fromisoformat(data[7]))
            self.disease = gender_birth[2].text_input("", placeholder="กรอกข้อมูลโรคประจำตัว", value=data[6])

            height_weight_radius = form.columns(2)
            height = height_weight_radius[0].number_input("ส่วนสูง (cm)", step=10.0, min_value=100.0, placeholder="(Ex. 170)", value=float(data[5]))
            weight = height_weight_radius[1].number_input("น้ำหนัก (kg)", step=1.0, placeholder="(Ex. 55)", value=float(data[4]))
            
            submit_col, cancel_col, _ = form.columns([0.1, 0.11, 0.7])
            submit = submit_col.form_submit_button("ตกลง", disabled=False) 
            cancel = cancel_col.form_submit_button("ยกเลิก", disabled=False)

            if submit:
                print("Submit")
                # self.on_editor(name, surname, gender, birth, self.disease, height, weight, data[0], form)

            if cancel:
                print("Clear")
                del st.session_state.SETTING
                st.rerun()

        else:
            del st.session_state.SETTING

    # Function to Setting Data
    def on_editor(self, name, surname, tasks):
        data = {
            "name": name,
            "surname": surname,
            "tasks": tasks
        }
        if all(value is not None for value in data.values()):
            # st.write(tasks)
            zero = [key for key, value in tasks.items() if not value]
            if len(zero) > 0:
                st.error("กรุณาใส่ข้อมูล" + " ".join(zero), icon="🚨")
            else:
                result = post_checklist(data)
                if "Success" in result["status"]:
                    st.success("บันทึกการตั้งค่าสำเร็จ!", icon="✅")
                    del st.session_state.tasks
                else:
                    st.error("ไม่สามารถบันทึกข้อมูลได้", icon="🚨")
        else:
            st.warning("โปรดกรอกข้อมูล", icon="⚠️")

if "register" not in st.session_state:
    update = Setting()
else:
    st.write("Login to Adjust your data")