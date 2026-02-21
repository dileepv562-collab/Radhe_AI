import streamlit as st
import google.generativeai as genai
from googlesearch import search
from gtts import gTTS
import os
import base64

# 1. Setup & Model
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    genai.configure(api_key="AIzaSyBpXf5sfUvA0xsKmYA2eajvw-8spYN7tm0")

model = genai.GenerativeModel('gemini-3-flash-preview')

# LIVE SEARCH FUNCTION
def get_live_data(query):
    search_results = ""
    try:
        for j in search(query, tld="co.in", num=3, stop=3, pause=2):
            search_results += f"\nSource: {j}"
        return search_results
    except:
        return ""

# Audio Function
def speak_now(text, speed):
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save("res.mp3")
        with open("res.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio><script>document.querySelector("audio").playbackRate = {speed};</script>'
            st.markdown(audio_html, unsafe_allow_html=True)
        os.remove("res.mp3")
    except: pass

# 2. UI Layers (Centered Circle)
st.markdown("""
    <style>
    .circle-container { display: flex; justify-content: center; padding: 20px; }
    .mantra-circle {
        width: 150px; height: 150px; border: 4px dashed #ff9933;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        animation: rotate 12s linear infinite; color: #cc5500; font-weight: bold;
        background: white; text-align: center;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="circle-container"><div class="mantra-circle">ओम नमो<br>भगवते<br>वासुदेवाय</div></div>', unsafe_allow_html=True)

# 3. Chat Logic
v_speed = st.sidebar.slider("वॉइस स्पीड", 1.0, 2.0, 1.5)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Radhe AI से ताज़ा जानकारी पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Live Search Trigger
        live_info = ""
        if any(word in prompt.lower() for word in ["price", "price", "news", "today", "current", "stock", "share"]):
            with st.spinner('इंटरनेट पर ताज़ा जानकारी ढूँढ रहा हूँ...'):
                live_info = get_live_data(prompt)
        
        context = f"Aap Radhe AI hain. Dilip ji ke liye ye live search data mila hai: {live_info}. Iska upyog karke sahi jawab dein."
        
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        speak_now(response.text, v_speed)
