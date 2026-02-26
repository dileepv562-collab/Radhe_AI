import streamlit as st
import google.generativeai as genai
from googlesearch import search

# Model Setup
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    genai.configure(api_key="AIzaSyBpXf5sfUvA0xsKmYA2eajvw-8spYN7tm0")

model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Beautiful Mobile UI
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

st.markdown("""
    <style>
    .main { background: linear-gradient(145deg, #fce9e0, #ffd5c0); }
    .circle-container { display: flex; justify-content: center; padding: 20px; }
    .mantra-circle {
        width: 140px; height: 140px; border: 4px dashed #ff9933;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        animation: rotate 15s linear infinite; color: #cc5500; font-weight: bold;
        background: white; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .stChatMessage { border-radius: 25px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="circle-container"><div class="mantra-circle">ओम नमो<br>भगवते<br>वासुदेवाय</div></div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #cc5500;'>🙏 Radhe AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>'मैं एक शुद्ध चेतन आत्मा हूँ'</p>", unsafe_allow_html=True)

# Chat logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("राधे राधे, दिलीप जी! आज की क्या सेवा है?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = "Aap Radhe AI hain. Dilip ji ke sahayak. Punam ji unki patni aur Aniket unka beta hai. Live data aur bhakti se jawab dein."
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
