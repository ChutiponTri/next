import streamlit as st
from datetime import date
from api_request import get_customer, post_edit

class Update():
    def __init__(self):
        self.header()
        self.sidebar()
        self.edit_form()

    # Function to Initialize Header
    def header(self):
        # Create Header Content
        st.header("Update Form", divider="rainbow")

    # Function to Initialize Sidebar
    def sidebar(self):
        pass

    # Function to Initialize Edit Form
    def edit_form(self):
        if "EDIT" not in st.session_state:
            name_col, sur_col = st.columns(2)
            with name_col:
                name_query = st.text_input("Enter Your Name", placeholder="Please Enter Your Name")
            with sur_col:
                surname_query = st.text_input("Enter Your Surname", placeholder="Please Enter Your Surame")
            button = st.button("Submit")
            if button:
                if len(name_query) > 1 and len(surname_query) > 1:
                    data = get_customer(name_query, surname_query)
                    print(data)
                    if "result" in data.keys():
                        if data["result"] is None:
                            st.write("None")
                            print("None")
                        if len(data["result"]) > 5:
                            st.session_state["EDIT"] = data["result"]
                            st.rerun()
                    else:
                        st.error("Cannot Find Data of %s %s" % (name_query, surname_query))
                else:
                    st.warning("Please Enter Valid Name")
        else:
            data = st.session_state["EDIT"]
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
                    self.on_editor(name, surname, gender, birth, self.disease, height, weight, data[0], form)

                if cancel:
                    print("Clear")
                    del st.session_state["EDIT"]
                    st.rerun()

            else:
                st.write(data)
                del st.session_state["EDIT"]
                # st.rerun()

    # Function to Update Data
    def on_editor(self, name, surname, gender, birth, disease, height, weight, id, form):
        data = {
            "id": id,
            "name": name.strip() if name != "" else None,
            "surname": surname.strip() if surname != "" else None,
            "gender": gender,
            "weight": weight if weight > 0 else None,
            "height": height if height > 100 else None,
            "disease": disease if disease != "" else None,
            "birth": str(birth)
        }
        if all(value is not None for value in data.values()):
            print("final", data)
            result = post_edit(data)
            print(result)
            if "Success" in result["status"]:
                form.success("แก้ไขข้อมูลผู้ใช้ %s สำเร็จ!" % name, icon="✅")
            else:
                form.error("ไม่สามารถแก้ไขข้อมูลได้", icon="🚨")
        else:
            # form.write(data)
            form.warning("โปรดกรอกข้อมูล", icon="⚠️")

update = Update()