import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. Page Config & CSS
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

st.markdown("""
    <style>
    .mantra-circle {
        width: 120px; height: 120px; border: 3px dashed #ff9933;
        border-radius: 50%; margin: auto; display: flex;
        align-items: center; justify-content: center;
        animation: rotate 15s linear infinite; color: #cc5500; font-weight: bold;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

# 2. Model Setup (Mera Fast Model)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.warning("Settings में API Key डालें।")

model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Audio Function with Speed Control
def speak_text(text, speed_factor):
    try:
        tts = gTTS(text=text, lang='hi', slow=False) # slow=False means fast speed
        tts.save("response.mp3")
        
        # Audio playback
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # Yahan speed control add kiya gaya hai
            md = f'<audio autoplay="true" controls style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        os.remove("response.mp3")
    except: pass

# 4. UI Layers
st.markdown('<div class="mantra-circle">ॐ नमो भगवते वासुदेवाय</div>', unsafe_allow_html=True)
st.title("🙏 Radhe AI")

# Speed Selector (Aap yahan se speed control kar sakte hain)
voice_speed = st.sidebar.slider("आवाज़ की रफ़्तार (Voice Speed)", 0.5, 2.0, 1.0)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Interaction
if prompt := st.chat_input("Radhe AI से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = "Aap Radhe AI hain, Dilip ji ke sahayak. Prem se jawab dein."
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Jawab ko turant sunayein
        speak_text(response.text, voice_speed)
        
