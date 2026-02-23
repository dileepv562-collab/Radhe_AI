import streamlit as st
import requests
import time

# --- SECURE SETUP ---
# Secrets se API Key lena (Security ke liye)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Kripya Streamlit Secrets mein 'GEMINI_API_KEY' set karein.")
    st.stop()

MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# --- DIVINE CIRCLE DESIGN ---
circle_html = """
<div style="text-align: center; color: gold; font-family: monospace; white-space: pre; line-height: 1.2;">
       .---.
    .'       '.
   /   OM NAMO  \\
  |  BHAGAVATE   |
   \\ VASUDEVAYA /
    '.       .'
       '---'
<h2 style="color: cyan;">ॐ नमो भगवते वासुदेवाय</h2>
</div>
"""
st.markdown(circle_html, unsafe_allow_html=True)
st.write(f"Radhe-Radhe Dilip Ji!] System Ready hai.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# User Input
if prompt := st.chat_input("Puchiye, Dilip ji..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Payload with 2026 Live Context
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Give a short Hindi reply for Dilip: {prompt}"}]}]
    }
    
    # Market keywords for Live Search
    if any(word in prompt.lower() for word in ['stoc', 'market', 'nifty', 'aaj', 'price']):
        payload["tools"] = [{"google_search_retrieval": {}}]
    
    # Retry Logic for weak network
    success = False
    with st.spinner("Radhe AI dhoodh raha hai..."):
        for i in range(2): 
            try:
                # 90s timeout
                response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=90)
                ans = response.json()['candidates'][0]['content']['parts'][0]['text']
                
                with st.chat_message("assistant"):
                    st.write(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                success = True
                break
            except:
                time.sleep(1)
                continue
    
    if not success:
        st.warning("Network weak hai. Ek baar refresh karke dobara try karein.")
        
