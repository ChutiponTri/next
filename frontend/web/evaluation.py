import streamlit as st
import pandas as pd

class Evaluation():
    def __init__(self):
        self.header()
        self.body()

    # Function to Create Header
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

        st.header("แบบประเมินภาระการดูแลผู้ป่วย", divider="rainbow")

    # Function to Create Body
    def body(self):
        questions = [
            "1. ท่านรู้สึกว่าผู้ป่วยร้องข้อความช่วยเหลือมากกว่าความต้องการจริง",
            "2. ท่านรู้สึกว่าท่านไม่มีเวลาเพียงพอสำหรับตัวเอง เนื่องจากว่าใช้เวลาในการดูแลผู้ป่วยมาก ไม่มีเวลาเป็นของตัวเอง",
            "3. ท่านรู้สึกมีความเครียดทั้งงานที่ต้องดูแลผู้ป่วย และงานอื่นที่ต้องรับผิดชอบ",
            "4. ท่านรู้สึกอึดอัดใจต่อพฤติกรรมของผู้ป่วย",
            "5. ท่านรู้สึกหงุดหงิดหรือโกรธ ขณะอยู่ใกล้ผู้ป่วย",
            "6. ท่านรู้สึกว่าผู้ป่วยทำให้ความสัมพันธ์ของท่านกับสมาชิกคนอื่นในครอบครัว หรือเพื่อนแย่ลง",
            "7. ท่านรู้สึกกลัวเกี่ยวกับสิ่งที่จะเกิดขึ้นในอนาคตกับผู้ป่วยซึ่งเป็นญาติของท่าน",
            "8. ท่านรู้สึกว่าผู้ป่วยต้องพึ่งพาท่าน",
            "9. ท่านรู้สึกตึงเครียดขขณะที่อยู่ใกล้ผู้ป่วย",
            "10. ท่านรู้สึกว่าสุขภาพของท่านไม่ค่อยดี เนื่องมาจากการดูแลผู้ป่วย",
            "11. ท่านรู้สึกว่าท่านไม่มีความเป็นส่วนตัวเท่าที่ต้องการ เนื่องจากการดูแลผู้ป่วย",
            "12. ท่านรู้สึกว่าท่านไม่สามารถมีสังคมได้ตามปกติ เนื่องจากการดูแลผู้ป่วย",
            "13. ท่านรู้สึกไม่สะดวกสบายในการติดต่อ คบหาเพื่อน เนื่องมาจากการดูแลผู้ป่วย",
            "14. ท่านรู้สึกว่าผู้ป่วยคาดหวังในตัวท่านมาก เสมือนมีท่านคนเดียวเท่านั้นที่พึ่งพาได้",
            "15. ท่านรู้สึกว่าท่านไม่มีเงินเพียงพอที่จะดูแลผู้ป่วย",
            "16. ท่านรู้สึกว่าท่านจะไม่สามารถอดทนดูแลผู้ป่วยได้อีกไม่นาน",
            "17. ท่านรู้สึกว่าท่านจะไม่สามารถควบคุมจัดการชีวิตตนเองได้ ตั้งแต่ดูแลผู้ป่วย",
            "18. ท่านอยากที่จะเลิกดูแลผู้ป่วยซึ่งเป็นญาติของท่าน และให้ผู้อื่นมาดูแลแทน",
            "19. ท่านรู้สึกว่าไม่มีอะไรที่มั่นคงแน่นอนเกี่ยวกับสิ่งที่ทำให้ผู้ป่วย",
            "20. ท่านรู้สึกว่าท่านควรจะได้รับการดูแลจากญาติคนอื่น",
            "21. ท่านรู้สึกว่าท่านน่าจะดูแลญาติของท่านได้ดีกว่านี้",
            "22. โดยภาพรวมท่านรู้สึกว่า การดูแลผู้ป่วยเป็นภาระสำหรับท่าน"
        ]

        scores = []
        col1, col2 = st.columns(2)
        for i, (question) in enumerate(questions):
            with st.container():  # Group question and feedback widget in a single container
                col1, col2 = st.columns([3, 1])  # Adjust column width ratios for better alignment
                col1.write(question)
                # star = col2.feedback("stars", key=f"val_{i}")  # Unique key for each widget
                star = col2.slider(f"ประเมินข้อที่ {i + 1}", 0, 4, 0, key=question)  # Unique key for each widget
                scores.append(star)
        if all(score is not None for score in scores):
            total = sum(scores)
            if total <= 20:
                burden = "ไม่มีหรือภาระน้อยมาก"
            elif total <= 40:
                burden = "ภาระเล็กน้อยถึงปานกลาง"
            elif total <= 60:
                burden = "ภาระปานกลางถึงรุนแรง"
            else:
                burden = "ภาระรุนแรง"
            st.subheader(f"คะแนนรวม {total}")
            st.html(
                f"""<div>
                    <p style="font-size: 1.5em;">{burden}</p>
                </div>
                """ 
            )
            st.button("บันทึก")
        else:
            st.html(
                """<div>
                    <p style="font-size: 1.5em;">กรุณากรอกข้อมูลทุกช่องก่อนบันทึก</p>
                </div>
                """
            )
        
    @staticmethod
    def temp():
        questions = [
            "1. ท่านรู้สึกว่าผู้ป่วยร้องข้อความช่วยเหลือมากกว่าความต้องการจริง",
            "2. ท่านรู้สึกว่าท่านไม่มีเวลาเพียงพอสำหรับตัวเอง เนื่องจากว่าใช้เวลาในการดูแลผู้ป่วยมาก ไม่มีเวลาเป็นของตัวเอง",
            "3. ท่านรู้สึกมีความเครียดทั้งงานที่ต้องดูแลผู้ป่วย และงานอื่นที่ต้องรับผิดชอบ",
            "4. ท่านรู้สึกอึดอัดใจต่อพฤติกรรมของผู้ป่วย",
            "5. ท่านรู้สึกหงุดหงิดหรือโกรธ ขณะอยู่ใกล้ผู้ป่วย",
        ]
        df = pd.DataFrame({
            "ภาระผู้ดูแล": questions,
            "ไม่เลย (0)" : [False for _ in range(22)],
            "นานครั้ง (1)" : [False for _ in range(22)],
            "บางครั้ง (2)" : [False for _ in range(22)],
            "บ่อยครั้ง (3)" : [False for _ in range(22)],
            "ประจำ (4)" : [False for _ in range(22)],
        })
        
        st.data_editor(
            df,
            column_config={
                "ไม่เลย (0)": st.column_config.CheckboxColumn(
                    "ไม่เลย (0)",
                    help="Select this option if it **doesn't apply** at all",
                    default=False,
                ),
                "นานครั้ง (1)" : st.column_config.CheckboxColumn(
                    "นานครั้ง (1)",
                    help="Select this option if it happens **occasionally**",
                    default=False,
                ),
                "บางครั้ง (2)" : st.column_config.CheckboxColumn(
                    "บางครั้ง (2)",
                    help="Select this option if it happens **sometimes**",
                    default=False,
                ),
                "บ่อยครั้ง (3)" : st.column_config.CheckboxColumn(
                    "บ่อยครั้ง (3)",
                    help="Select this option if it happens **often**",
                    default=False,
                ),
                "ประจำ (4)" : st.column_config.CheckboxColumn(
                    "ประจำ (4)",
                    help="Select this option if it happens **frequently**",
                    default=False,
                ),
            },
            disabled=["widgets"],
            hide_index=True,
        )


tele = Evaluation()