import streamlit as st
import requests

# --- Setup ---
# API Key ab Streamlit ke secrets se aayegi
API_KEY = st.secrets["API_KEY"] 
MODEL = "gemini-2.5-flash-lite" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# UI setup
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")
st.title("🕉️ Radhe AI: आपका डिजिटल साथी")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("श्री हरि को कुछ पूछें..."):
    # User message display
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare chat history for API (Context Memory)
    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": msg["content"]}]})

    # API Request with History and Tools
    payload = {
        "contents": history,
        "tools": [{"google_search": {}}]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        if 'candidates' in result:
            ai_text = result['candidates'][0]['content']['parts'][0]['text']
            with st.chat_message("assistant"):
                st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
        else:
            st.error("Radhe AI अभी ध्यान लगा रहे हैं, कृपया पुनः प्रयास करें।")
            
    except Exception as e:
        st.error(f"सिस्टम त्रुटि: {e}")
        
