import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. Page Config & CSS (Layers with Circle)
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

st.markdown("""
    <style>
    .mantra-circle {
        width: 120px; height: 120px; border: 3px dashed #ff9933;
        border-radius: 50%; margin: auto; display: flex;
        align-items: center; justify-content: center;
        animation: rotate 10s linear infinite; color: #cc5500; font-weight: bold;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .stButton>button { background-color: #ff9933; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Gemini 3 Flash Model Setup
try:
    # Secrets se API key uthana
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    # Agar secrets nahi hai toh backup key
    genai.configure(api_key="AIzaSyBpXf5sfUvA0xsKmYA2eajvw-8spYN7tm0")

# Sabse naya Gemini 3 Flash model
model = genai.GenerativeModel('gemini-3-flash-preview')

# 3. Super-Fast Audio Function
def speak_now(text, speed):
    try:
        # gTTS ko fast mode me chalana
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save("fast_res.mp3")
        
        with open("fast_res.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # HTML5 Audio me speed parameters set karna
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

# 4. UI Layers
st.markdown('<div class="mantra-circle">ॐ नमो भगवते वासुदेवाय</div>', unsafe_allow_html=True)
st.title("🙏 Radhe AI: High-Speed Mode")

# Voice Speed Control in Sidebar
st.sidebar.header("वॉइस सेटिंग्स")
v_speed = st.sidebar.slider("बोलने की रफ़्तार", 2.0, 3.0, 2.0, step=0.2)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Fast Interaction
if prompt := st.chat_input("Radhe AI से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Context for Dilip ji
        context = "Aap Radhe AI hain. User Dilip hain jo subah 4 AM sadhna karte hain. Unka mantra Om Yogmaya Mahalakshmi Narayani Namostute hai. Punam ji unki patni hain. Turant aur fast jawab dein."
        
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Audio playback with selected speed
        speak_now(response.text, v_speed)
        
