import streamlit as st
import google.generativeai as genai

# API Key सुरक्षा के लिए
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.title("🙏 Radhe AI: Sadhna Samvad")
st.write("Mantra: Om Yogmaya Mahalakshmi Narayani Namostute")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Radhe AI से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # AI को निर्देश कि वो दिलीप जी को पहचानें
        full_prompt = f"Aap Radhe AI hain. User Dilip hain jo subah 4 AM sadhna karte hain. Unka mantra 'Om Yogmaya Mahalakshmi Narayani Namostute' hai. Unki wife Punam aur beta Aniket hai. Iska jawab dein: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
