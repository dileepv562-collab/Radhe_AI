import streamlit as st
import requests
import time

# --- SECURE SETUP ---
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Design
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Radhe-Radhe Dilip Ji!]</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Puchiye, Dilip ji..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Give a short Hindi response for Dilip: {prompt}"}]}]
    }
    
    if any(word in prompt.lower() for word in ['stoc', 'market', 'nifty', 'aaj', 'rate']):
        payload["tools"] = [{"google_search_retrieval": {}}]
    
    # --- AUTO-RETRY LOGIC ---
    success = False
    with st.spinner("Radhe AI जवाब ढूँढ रहा है..."):
        for i in range(3): # 3 baar koshish karega
            try:
                # Timeout ko 100 seconds kar diya
                response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=100)
                ans = response.json()['candidates'][0]['content']['parts'][0]['text']
                
                with st.chat_message("assistant"):
                    st.write(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                success = True
                break
            except Exception as e:
                time.sleep(2) # 2 second rukk kar fir koshish
                continue
    
    if not success:
        st.error("Signal area mein jayein aur ek baar Refresh karein.")
           
