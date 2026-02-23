import streamlit as st
import requests

# --- CONFIG ---
API_KEY =
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Header
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Radhe-Radhe Dilip Ji!]</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sabse Tez Logic: No Search unless strictly requested
if prompt := st.chat_input("Hii likhkar check karein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Base Instruction: Isse AI fast reply dega
    payload = {
        "contents": [{"parts": [{"text": f"Aap Radhe AI hain. Dilip ji se baat kar rahe hain. Hindi mein short reply dein: {prompt}"}]}]
    }
    
    # Google Search tabhi chalega jab aap 'live' ya 'stock' likhenge
    if any(word in prompt.lower() for word in ['live', 'stock', 'rate', 'aaj', 'price']):
        payload["tools"] = [{"google_search_retrieval": {}}]
    
    try:
        # Request with 90s timeout for very slow networks
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=90)
        ans = response.json()['candidates'][0]['content']['parts'][0]['text']
        st.session_state.messages.append({"role": "assistant", "content": ans})
    except:
        st.error("Network bohot weak hai. Ek baar Airplane mode on-off karke try karein.")

# Messages display
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        
