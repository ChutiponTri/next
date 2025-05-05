import streamlit as st
from api_request import post_requests, get_requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
import time
import os

# Load environment variables
load_dotenv()

class Assistance():
    def __init__(self):
        # Set up the LLM model
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.getenv("GEMINI_KEY"))

        # chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "preview" not in st.session_state:
            st.session_state.preview = True

        self.header()
        self.chat_tab()

    # Function to Display Header
    def header(self):
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

        st.header("Housepital Chat", divider="rainbow")
        if len(st.session_state.messages) == 0:
            long_text = """
            <p>
                Welcome to <strong>Housepital Care</strong> - your AI-powered health assistant. 
                This chatbot simulates a medical interview
                where an AI doctor provides feedback based on your symptoms, asks follow-up questions,
                and helps guide you toward better health decisions.
                You can learn more about the Housepital Care by visiting our site.
            </p>
            """
            with st.container():
                st.html(long_text)
                          
        self.user_input = st.chat_input("ถามคำถามได้เลย: ...")
        if self.user_input:
            self.message(self.user_input)

    # Function to Create Message
    def message(self, message):
        st.session_state.messages.append(HumanMessage(content=message))

        # Construct prompt with context
        prompt = f"""You are a professional and empathetic medical doctor name's Dr.Housepital conducting patient interviews. 
            Your role is to:
            - Carefully interpret the patient's health data or description.
            - Provide medical feedback in a respectful and informative way.
            - Ask relevant follow-up questions to gather more information.
            - Avoid making direct diagnoses, but suggest what the symptoms could indicate.
            - Encourage appropriate medical testing or lifestyle adjustments where applicable.

            Always maintain a warm, professional, and supportive tone. Here is user input
            {message}
        """

        # Generate response
        self.response = self.llm.invoke([HumanMessage(content=prompt)])
        
    # Function to Display ChatUI
    def chat_tab(self):  
        for msg in st.session_state.messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            with st.chat_message(role):
                st.write(msg.content)
        if self.user_input:
            with st.chat_message("assistant"):
                st.write_stream(self.stream_data(self.response.content))
                st.session_state.messages.append(AIMessage(content=self.response.content))

    # Function to Write Stream Message
    def stream_data(self, data:str):
        for word in data:
            yield word
            time.sleep(0.005)

if __name__ == "__main__":
    app = Assistance()