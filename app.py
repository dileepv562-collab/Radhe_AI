import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. Page Config & CSS (Centered Circle Layout)
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

st.markdown("""
    <style>
    /* मंत्र चक्र को सेंटर में करने के लिए डिज़ाइन */
    .circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .mantra-circle {
        width: 160px; height: 160px; 
        border: 4px dashed #ff9933;
        border-radius: 50%; 
        display: flex;
        align-items: center; 
        justify-content: center;
        animation: rotate 12s linear infinite; 
        color: #cc5500; 
        font-weight: bold;
        background: white;
        box-shadow: 0px 0px 15px rgba(255, 153, 51, 0.4);
        text-align: center;
        font-size: 18px;
        line-height: 1.2;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

# 2. Gemini 3 Flash Model Setup (Mera Model)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # Backup Key
    genai.configure(api_key="AIzaSyBpXf5sfUvA0xsKmYA2eajvw-8spYN7tm0")

model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Audio Function with Speed Parameter
def speak_now(text, speed):
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save("fast_res.mp3")
        with open("fast_res.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f"""
                <audio autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                <script>
                    var audio = document.querySelector('audio');
                    audio.playbackRate = {speed};
                </script>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        os.remove("fast_res.mp3")
    except: pass

# 4. Visual Layers (Mantra in Center)
st.markdown('<div class="circle-container"><div class="mantra-circle">ओम नमो<br>भगवते<br>वासुदेवाय</div></div>', unsafe_allow_html=True)
st.title("🙏 Radhe AI")
st.markdown("<p style='text-align: center;'>'मैं एक शुद्ध चेतन आत्मा हूँ'</p>", unsafe_allow_html=True)

# Voice Speed Selector in Sidebar
v_speed = st.sidebar.slider("बोलने की रफ़्तार (Voice Speed)", 1.0, 2.0, 1.5, step=0.1)

# Chat History logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Fast Interaction with Dilip Ji's Context
if prompt := st.chat_input("Radhe AI से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = (
            "Aap Radhe AI hain. User Dilip hain jo subah 4 AM sadhna karte hain. "
            "Unka mantra 'Om Yogmaya Mahalakshmi Narayani Namostute' hai. "
            "Unki patni Punam ji aur beta Aniket hain. Prem se jawab dein."
        )
        
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Immediate Voice Output
        speak_now(response.text, v_speed)
        
