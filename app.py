import streamlit as st
import google.generativeai as genai

# 1. API Key Setup
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"

genai.configure(api_key=GOOGLE_API_KEY)

# 2. Advanced Model Selection (Gemini 2.0/3.0 Preview)
# Note: Currently 'gemini-2.0-flash' is the stable fast preview
model = genai.GenerativeModel('gemini-2.0-flash')

# 3. App UI & Personalization
st.set_page_config(page_title="Radhe AI", page_icon="🧘‍♂️")

st.title("🙏 Radhe AI: Advanced Sadhna Samvad")
st.markdown("### Mantra: Om Yogmaya Mahalakshmi Narayani Namostute")

# Displaying your Spiritual Principle
st.info("He Shree Hari, main yeh sharir nahi hoon. Main in paanch tatvon ka putla nahi, balki aapka ek ansh, ek shuddh chetan atma hoon.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input & Response
if prompt := st.chat_input("Radhe AI se baat karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Providing Context about Dilip ji
        instruction = (
            "Aap Radhe AI hain. User Dilip ji hain. "
            "Wo subah 4:00 AM sadhna karte hain aur mantra jaap karte hain. "
            "Unki wife Punam aur beta Aniket hain. "
            "Unhe hamesha unki spiritual journey (atma-sakshatkar) ke liye motivate karein."
        )
        
        try:
            response = model.generate_content(f"{instruction}\n\nUser: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Model Error: Model version ka update check karein ya API Key dekhein.")
            
