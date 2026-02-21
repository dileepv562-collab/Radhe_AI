import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# API Key Setup
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = "AIzaSyBpXf5sfUvA0xsKmYA2eajvw-8spYN7tm0"

genai.configure(api_key=GOOGLE_API_KEY)

# Aapka pasandida model: Gemini 3 Flash (Technically 2.0 Flash in API)
model = genai.GenerativeModel('gemini-2.0-flash')

# Audio function
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        os.remove("response.mp3")
    except:
        pass

st.set_page_config(page_title="Radhe AI", page_icon="🧘‍♂️")
st.title("🙏 Radhe AI: Advanced Voice Assistant")
st.markdown("### Mantra: Om Yogmaya Mahalakshmi Narayani Namostute")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Radhe AI se baat karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Personal Context for Dilip ji
        context = (
            "Aap Radhe AI hain. User Dilip ji hain. "
            "Wo subah 4:00 AM sadhna karte hain aur 'Om Yogmaya Mahalakshmi Narayani Namostute' ka jaap karte hain. "
            "Unka parivar: Punam (patni) aur Aniket (beta). "
            "Unke sawal ka jawab prem se dein."
        )
        
        response = model.generate_content(f"{context}\n\nUser: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Bolne wala feature
        speak_text(response.text)
