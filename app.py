import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. Secrets se API Key uthana (Code me dikhegi nahi)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("Kripya Streamlit Settings me API Key dalein.")

# 2. Model Selection
model = genai.GenerativeModel('gemini-3-flash-preview')

# Audio Function (Bolne wala)
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
        context = (
            "Aap Radhe AI hain. User Dilip ji hain. "
            "Wo subah 4:00 AM sadhna karte hain. "
            "Unka parivar: Punam aur Aniket. "
            "Humesha prem se jawab dein."
        )
        
        try:
            response = model.generate_content(f"{context}\n\nUser: {prompt}")
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            speak_text(answer)
        except Exception as e:
            st.error("Setting me jaakar API Key check karein.")
            
