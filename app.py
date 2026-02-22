import streamlit as st
import requests
import json

# --- SETUP ---
API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# Streamlit Page Design
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Circle
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_content_html=True)
st.subheader("Radhe-Radhe Dilip Ji!]")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Radhe AI se taaza jankari poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2026 Live Data Search
    payload = {
        "contents": [{"parts": [{"text": f"Current date: Feb 2026. Use Google Search for Dilip: {prompt}"}]}],
        "tools": [{"google_search_retrieval": {}}]
    }

    try:
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload)
        result = response.json()
        
        if 'candidates' in result:
            full_response = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"System Error: {e}")
