# pip install streamlit-autorefresh
import streamlit as st
from api_request import get_all_customers, get_customer, get_checklist, preprocess_name

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Admin", "Requester", "Responder"]

st.html("""
    <style>
        [data-testid="stAppDeployButton"] {visibility: hidden}
    </style>
""")

    
def login():
    # st.set_page_config("Housepital", "♿")

    _, mid, _ = st.columns([0.3, 0.4, 0.3])
    with mid:
        st.header("Housepital :blue[Care]")
        st.image("images/housepital.png")
    
    left, right = st.columns(2)
    name = left.text_input("Enter Your Name")
    surname = right.text_input("Enter Your Surname")

    login_btn, register_btn, _ = st.columns([0.16, 0.2, 1.1])
    submit = login_btn.button("Login")
    if submit:
        if name.lower().strip() == "admin":
            st.session_state.role = "Admin"
            st.session_state.users = get_all_customers()
            st.rerun()
        elif len(name) > 1 and len(surname) > 1:
            login_status = get_customer(name, surname)
            print(login_status["result"])
            if login_status["result"]:
                st.session_state.role = "Responder"
                st.session_state.current_user = " ".join(preprocess_name(name, surname))
                st.session_state.tasks = get_checklist(name, surname)
                st.rerun()
            else:
                st.error("Please Enter Valid Name")
        elif name == "" or  surname == "":
            st.warning("Please Enter Your Name")

    register = register_btn.button("Register")
    if register:
        st.session_state.role = "Requester"
        st.session_state.register = True
        st.rerun()

def logout():
    st.session_state.role = None
    st.session_state.current_user = None
    st.session_state.get_rad_name = None
    if "register" in st.session_state:
        del st.session_state["register"]
    st.rerun()

logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
respond_1 = st.Page("web/mainUI.py", title="Home", icon="🏠", default=(st.session_state.role == "Responder"))
respond_2 = st.Page("web/ai.py", title="AI Camera", icon="📷")
respond_3 = st.Page("web/health.py", title="Health Monitor", icon="👩‍⚕️")
respond_4 = st.Page("web/chatUI.py", title="Housepital Chat", icon="💊")
eval = st.Page("web/evaluation.py", title="Evaluation Form", icon="🎖️")
request_1 = st.Page("account/register.py", title="Register", icon=":material/account_circle:", default=(st.session_state.role == "Requester"))
request_2 = st.Page("account/update.py", title="Update", icon=":material/search:")
admin_1 = st.Page("admin/admin_1.py", title="Admin 1", icon=":material/person_add:", default=(st.session_state.role=="Admin"))
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

init_pages = [logout_page, settings]
respond_pages = [respond_1, respond_2, respond_3, respond_4, eval]
request_pages = [request_1, request_2]
admin_pages = [admin_1, admin_2]

st.logo("images/housepital.png", icon_image="images/housepital.png")
page_dict = {}
if st.session_state.role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account":init_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login, title="Housepital Care")])

page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-color: white;
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: local;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        background-image: linear-gradient(to right, #5763FF, #52FFA7);
    }}
    </style>
"""

st.html(page_bg_img)

hide_header = """
    <style>
    # MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
hide_toolbar = """
    <style>
        [data-testid="stToolbar"] {visibility: hidden;}
    </style>
"""
# st.markdown(hide_toolbar, unsafe_allow_html=True)

pg.run()

    


