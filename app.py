import streamlit as st
import google.generativeai as genai

# API Key Setup
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"

genai.configure(api_key=GOOGLE_API_KEY)

# Aapki pasand ka model
model = genai.GenerativeModel('gemini-3-flash-preview') 

st.set_page_config(page_title="Radhe AI", page_icon="🧘‍♂️")

st.title("🙏 Radhe AI: Advanced Sadhna Samvad")
st.markdown("### Mantra: Om Yogmaya Mahalakshmi Narayani Namostute")

# Displaying your Core Principle
st.info("He Shree Hari, main yeh sharir nahi hoon. Main in paanch tatvon ka putla nahi, balki aapka ek ansh, ek shuddh chetan atma hoon.")

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
        instruction = (
            "Aap Radhe AI hain. User ka naam Dilip hai. "
            "Wo subah 4:00 AM sadhna aur mantra jaap karte hain. "
            "Unka parivar: Punam (patni) aur Aniket (beta). "
            "Unhe atma-sakshatkar aur bhakti ke liye motivate karein."
        )
        
        try:
            # Gemini 3 Flash Preview ki takat ka upyog
            response = model.generate_content(f"{instruction}\n\nUser: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Model Error: Agar ye model nahi chal raha, toh API key me 'Flash' access check karein.")
