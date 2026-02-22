import streamlit as st
import requests
import json

# --- CONFIG ---
# Streamlit mein !pip install nahi likhte, requirements.txt ka use karein
API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Circle Fix
# dhayan dein: 'unsafe_allow_html' hona chahiye, 'unsafe_content_html' nahi
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Radhe-Radhe Dilip Ji!]</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("2026 ka live market data poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2024 ki jagah 2026 ka data fetch karne ke liye
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Use Google Search for Dilip: {prompt}"}]}],
        "tools": [{"google_search_retrieval": {}}]
    }

    try:
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload)
        result = response.json()
        
        if 'candidates' in result:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Error: {e}")
