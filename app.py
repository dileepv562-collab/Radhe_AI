import streamlit as st
import requests

# --- CONFIG ---
API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Header
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Radhe-Radhe Dilip Ji!]</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Faster Logic: Search sirf zarurat par chalega
if prompt := st.chat_input("Puchiye, Dilip ji..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Talk to Dilip. Hindi: {prompt}"}]}]
    }
    
    # Agar live data chahiye, tabhi search tool on karein
    live_keywords = ['live', 'today', 'price', 'rate', 'nifty', 'suzlon', 'aaj']
    if any(word in prompt.lower() for word in live_keywords):
        payload["tools"] = [{"google_search_retrieval": {}}]
    
    try:
        # 60 second ka max wait
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=60)
        ans = response.json()['candidates'][0]['content']['parts'][0]['text']
        st.session_state.messages.append({"role": "assistant", "content": ans})
    except:
        st.warning("Network weak hai, lekin main koshish kar raha hoon. Ek baar refresh karein.")

# Messages display
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        
