import streamlit as st
import requests
import time

# --- SECURE SETUP ---
# Secrets se API Key lena zaruri hai
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# --- CLASSIC DIVINE CIRCLE ---
circle_html = """
<div style="text-align: center; color: #FFD700; font-family: 'Courier New', monospace; white-space: pre; font-weight: bold;">
       .---.
    .'       '.
   /   OM NAMO  \\
  |  BHAGAVATE   |
   \\ VASUDEVAYA /
    '.       .'
       '---'
<h2 style="color: #00FFFF; text-shadow: 2px 2px #000;">ॐ नमो भगवते वासुदेवाय</h2>
</div>
"""
st.markdown(circle_html, unsafe_allow_html=True)
st.write(f"Radhe-Radhe Dilip Ji!] System Ready hai.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display logic
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Smart Input with No-Error Logic
if prompt := st.chat_input("Puchiye, Dilip ji..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2026 ka live context aur Google Search
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Give a short Hindi reply for Dilip: {prompt}"}]}]
    }
    
    # Live stock market check
    if any(word in prompt.lower() for word in ['stoc', 'market', 'nifty', 'aaj', 'rate']):
        payload["tools"] = [{"google_search_retrieval": {}}]

    with st.chat_message("assistant"):
        response_placeholder = st.empty() # Khali jagah jahan ek-ek shabd dikhega
        full_response = ""
        
        try:
            # 150 seconds ka maximum wait
            response = requests.post(URL, json=payload, timeout=150)
            result = response.json()
            
            if 'candidates' in result:
                ans_text = result['candidates'][0]['content']['parts'][0]['text']
                
                # Streaming effect: Ek-ek shabd karke dikhayega
                for word in ans_text.split():
                    full_response += word + " "
                    time.sleep(0.05)
                    response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("AI thoda vyast hai, 1 minute rukk kar koshish karein.")
        except:
            st.warning("Internet bohot zyada slow hai. Kripya page refresh karke ek chota message (jaise 'Hi') bhejein.")
            
