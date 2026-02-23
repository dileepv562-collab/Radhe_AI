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

# Messages dikhane ke liye loop
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# User Input Logic
if prompt := st.chat_input("Puchiye, Dilip ji..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Instruction for AI
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Give a short Hindi response for Dilip: {prompt}"}]}]
    }
    
    # Smart Recognition: Stock ya Market ki baaton par Live Search on
    market_words = ['stoc', 'stock', 'market', 'nifty', 'price', 'rate', 'aaj']
    if any(word in prompt.lower() for word in market_words):
        payload["tools"] = [{"google_search_retrieval": {}}]
    
    try:
        # 120s timeout slow internet ke liye
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=120)
        ans = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        with st.chat_message("assistant"):
            st.write(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
    except:
        st.error("Network bohot weak hai. Ek baar Airplane mode try karein.")
        
