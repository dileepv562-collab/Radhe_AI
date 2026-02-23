import streamlit as st
import requests

# --- SECURE SETUP ---
# Yeh line Streamlit ke 'Secrets' se aapki chabi apne aap utha legi
API_KEY = st.secrets["GEMINI_API_KEY"]
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# Divine Design
st.markdown("<h1 style='text-align: center; color: gold;'>🕉️ OM NAMO BHAGAVATE VASUDEVAYA 🕉️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Radhe-Radhe Dilip Ji!]</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhane ke liye
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# User Input
if prompt := st.chat_input("Puchiye, Dilip ji..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 2026 ka live context
    payload = {
        "contents": [{"parts": [{"text": f"Today is Feb 2026. Give a short Hindi response for Dilip: {prompt}"}]}]
    }
    
    # Live data search logic
    if any(word in prompt.lower() for word in ['stoc', 'market', 'nifty', 'aaj', 'price', 'rate']):
        payload["tools"] = [{"google_search_retrieval": {}}]
    
    try:
        # Long timeout for slow internet
        response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=90)
        ans = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        with st.chat_message("assistant"):
            st.write(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
    except:
        st.warning("Network weak hai. Ek baar refresh karein.")
        
