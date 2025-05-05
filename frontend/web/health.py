import streamlit as st
from api_request import post_health

class Calculation():
    def __init__(self):
        self.header()
        self.style()
        self.sidebar()
        self.body()

    # Function to Create Header
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

        st.header("ระบบประเมินสุขภาพผู้ป่วยเบื้องต้น", divider="rainbow")

    # Function to Create Style
    def style(self):
        text = """
        <style>
            .calc_right {
                text-align: right;
            }
            .questions {
                display: flex; 
                justify-content: space-between; 
                align-items: center;
            }
            .par, .head {
                font-size: 24px;
            }

            [data-testid="stMarkdownContainer"] > p {
                font-size: 18px;
            }

            [class="st-af st-co st-cp st-cq st-cr st-cs st-ct"] {
                display: flex;
                gap: 10px;
            }
        </style>

        <div class="calc_left">
            <u class="head">โรคปอดติดเชื้อ</u><br>
            <u class="head">ประเมินความเสี่ยง</u>
        </div>
        <div class="calc_right">
            <p class="par">CBR-65 Score</p>
        </div>
        <div class="calc_left">
            <p class="par">คุณมีอาการเหล่านี้หรือไม่</p>
        </div>
        """
        st.html(text)

    # Function to Create Sidebar
    def sidebar(self):
        pass

    # Function to Create Body
    def body(self):
        score = 0
        options = ["ใช่", "ไม่ใช่"]

        confuse = st.pills("สับสน", options=options, selection_mode="single", key="confuse")
        breath = st.pills("หายใจ 1 นาทีมากกว่า 30 ครั้ง", options=options, selection_mode="single", key="breath")
        pressure = st.pills("ความดัน น้อยกว่า 90/60", options=options, selection_mode="single", key="pressure")
        age = st.pills("อายุ มากกว่า 65", options=options, selection_mode="single", key="age")

        for choice in [confuse, breath, pressure, age]:
            if choice == "ใช่":
                score += 1

        st.markdown("---")
        st.markdown("<u>คะแนนรวม %d</u>" % (score), unsafe_allow_html=True)

        if score == 0:
            advice = ""
        elif score == 1:
            advice = "ควรดูแลตัวเอง"
        elif score == 2:
            advice = "เริ่มมีความเสี่ยงด้านสุขภาพ"
        elif score == 3:
            advice = "ควรพบแพทย์"
        elif score == 4:
            advice = "ควรพบแพทย์อย่างเร่งด่วน"

        st.write(advice)

        if st.button("ตกลง") and "current_user" in st.session_state:
            name, surname = self.fullname.split(" ")
            data = {    
                "name": name,
                "surname": surname,
                "evaluate_score": score,
                "descr": advice
            }
            result = post_health(data)
            if "status" in result.keys():
                if "Success" in result["status"]:
                    st.success("บันทึกข้อมูลสำเร็จ")
                else:
                    st.error(result["status"])
            else:
                st.error("ไม่สำเร็จ")

calc = Calculation()


