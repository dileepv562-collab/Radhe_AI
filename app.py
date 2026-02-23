import streamlit as st
import requests
from streamlit_mic_recorder import speech_to_text

# --- SECURE SETUP ---
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI Voice", page_icon="🕉️")

# --- DIVINE DESIGN ---
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.write(f"Radhe-Radhe Dilip Ji!] Bolkar puchiye.")

# --- VOICE INPUT FEATURE ---
# Yeh button aapki awaaz ko text mein badal dega
text = speech_to_text(language='hi', start_prompt="🎤 Bolne ke liye dabayein", key='speech')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Agar awaaz se text milta hai toh usse prompt banayein
if text:
    prompt = text
else:
    prompt = st.chat_input("Ya yahan type karein...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Give a short Hindi reply: {prompt}"}]}]
    }
    
    # Live data search logic
    if any(word in prompt.lower() for word in ['nifty', 'market', 'stoc', 'aaj', 'price']):
        payload["tools"] = [{"google_search_retrieval": {}}]

    with st.spinner("Radhe AI sun raha hai..."):
        try:
            response = requests.post(URL, json=payload, timeout=120)
            ans = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except:
            st.error("Network weak hai, dobara bolyein.")

# Chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        
