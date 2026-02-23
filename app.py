import streamlit as st
import requests

# --- CONFIG ---
API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"
MODEL = ('gemini-3-flash-preview')
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Header
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.write("Radhe-Radhe Dilip Ji!]")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Logic
if prompt := st.chat_input("2026 ka live data poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2026 Live Search Tool
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Search live for Dilip: {prompt}"}]}],
        "tools": [{"google_search_retrieval": {}}]
    }
    
    try:
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload)
        ans = response.json()['candidates'][0]['content']['parts'][0]['text']
        st.session_state.messages.append({"role": "assistant", "content": ans})
    except:
        st.error("Internet slow hai, dobara try karein.")

# Messages dikhayein
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
