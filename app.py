import streamlit as st
import google.generativeai as genai

# 1. API Key Setup (Secrets se ya Direct)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # Agar secrets set nahi hai toh ye key use hogi
    GOOGLE_API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"

genai.configure(api_key=GOOGLE_API_KEY)

# 2. Model Setup (Naya aur Tez Model)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Page Configuration
st.set_page_config(page_title="Radhe AI", page_icon="🧘‍♂️")

st.title("🙏 Radhe AI: Sadhna Samvad")
st.markdown("### Mantra: Om Yogmaya Mahalakshmi Narayani Namostute")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input and AI Response
if prompt := st.chat_input("Radhe AI se baat karein..."):
    # User ka message save karein
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # AI ko aapka context dena (Dilip ji ki jankari)
        instruction = (
            "Aap Radhe AI hain, Dilip ji ke sahayak. "
            "Dilip ji subah 4:00 AM sadhna karte hain. "
            "Unka mantra 'Om Yogmaya Mahalakshmi Narayani Namostute' hai. "
            "Unki patni ka naam Punam hai aur bete ka naam Aniket hai. "
            "Humesha prem se aur adhyatmik dhang se jawab dein."
        )
        
        # Response generate karna
        try:
            response = model.generate_content(f"{instruction}\n\nUser: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: API Key check karein ya thoda intezar karein. {e}")
