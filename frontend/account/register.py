import streamlit as st
from datetime import date
from api_request import get_requests, post_requests, post_register, post_checklist

class Registration():
    def __init__(self):
        self.header()
        self.sidebar()
        self.regiter_form()

    # Function to Initialize Header
    def header(self):
        # Create Header Content
        st.header("ลงทะเบียน", divider="rainbow")

    # Function to Initialize Sidebar
    def sidebar(self):
        pass

    # Function to Initialize Register Form
    def regiter_form(self):
        # Create Input Register Form
        form = st.form("ฟอร์มลงทะเบียน")
        name_surname = form.columns(2)
        name = name_surname[0].text_input("ชื่อ", placeholder="กรอกชื่อ", value="")
        surname = name_surname[1].text_input("นามสกุล", placeholder="กรอกนามสกุล", value="")

        gender_birth = form.columns(3)
        gender = gender_birth[0].selectbox("เพศ", ["ชาย", "หญิง", "ไม่ระบุ"], index=0)
        birth = gender_birth[1].date_input("วันเดือนปีเกิด", min_value=date(1900, 1, 1))
        disease = gender_birth[2].text_input("โรคประจำตัว", placeholder="กรอกข้อมูลโรคประจำตัว")
            
        height_weight_radius = form.columns(2)
        height = height_weight_radius[0].number_input("ส่วนสูง (cm)", step=10, min_value=100, placeholder="(Ex. 170)")
        weight = height_weight_radius[1].number_input("น้ำหนัก (kg)", step=1, placeholder="(Ex. 55)")

        submit = form.form_submit_button("ลงทะเบียน", disabled=False)

        if submit:
            self.on_register(name, surname, gender, birth, disease, height, weight, form)
                    
    # Function to Register
    def on_register(self, name, surname, gender, birth, disease, height, weight, form):
        data = {
            "name": name.strip() if name != "" else None,
            "surname": surname.strip() if surname != "" else None,
            "gender": gender,
            "weight": weight if weight > 0 else None,
            "height": height if height > 100 else None,
            "disease": disease.strip(),
            "birth": str(birth)
        }

        if all(value is not None for value in data.values()):
            result = post_register(data)
            if "status" in result.keys():
                if "Success" in result["status"]:
                    check_list = {
                        "name": data["name"],
                        "surname": data["surname"],
                        "tasks": {
                            "ช่วงเช้า": ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "ตรวจแผลกดทับ", "ยาก่อน/หลังอาหาร"],
                            "ก่อนเที่ยง": ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "ตรวจแผลกดทับ", "ยาก่อน/หลังอาหาร"],
                            "ช่วงกลางวัน": ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "ตรวจแผลกดทับ", "ยาก่อน/หลังอาหาร"],
                            "ช่วงเย็น": ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "ตรวจแผลกดทับ", "ยาก่อน/หลังอาหาร"],
                            "ตอนค่ำ": ["วัดอัตราการเต้นของหัวใจ", "วัดความดันเลือด", "วัดระดับน้ำตาลในเลือด", "ตรวจแผลกดทับ", "ยาก่อน/หลังอาหาร"],
                        }
                    }
                    upsert = self.upsert_checklist(check_list)
                    if upsert:
                        form.success("ผู้ใช้ %s ลงทะเบียนสำเร็จ" % name, icon="✅")
                    else:
                        form.warning("ไม่สามารถสร้าง Check List ได้", icon="⚠️")
                else:
                    form.warning("ไม่สามารถลงทะเบียนได้ %s" % result["status"], icon="⚠️")
            else:
                form.error("ลงทะเบียนไม่สำเร็จ", icon="🚨")
        else:
            # form.write(data)
            form.warning("โปรดใส่ข้อมูลทั้งหมด", icon="⚠️")

    # Function to Create Initial Check-List
    def upsert_checklist(self, data):
        result = post_checklist(data)
        if type(result) == dict:
            if "status" in result.keys():
                if "Success" in result["status"]:
                    return True
        return False

register = Registration()