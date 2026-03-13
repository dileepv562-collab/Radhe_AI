import streamlit as st
import requests

# --- 1. Page & UI Setup ---
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# CSS for the Circle UI
st.markdown("""
<style>
    .radhe-circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .radhe-circle-border {
        width: 250px;
        height: 250px;
        border-radius: 50%;
        border: 4px solid #cc5500;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: transparent;
    }
    .radhe-circle-text {
        text-align: center;
        color: #DAA520;
        font-weight: bold;
        font-size: 1.3em;
        line-height: 1.2;
    }
</style>

<div class="radhe-circle-container">
    <div class="radhe-circle-border">
        <div class="radhe-circle-text">
            OM NAMO<br>
            BAGVATE<br>
            VASUDEVAY
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🕉️ Radhe AI: आपका डिजिटल सहायक")

# --- 2. Functions (Tools) ---

def search_youtube(query):
    """यूट्यूब पर वीडियो खोजने के लिए टूल"""
    url = f"https://www.youtube.com/results?search_query={query}"
    return f"मैंने यूट्यूब पर '{query}' के लिए खोज की है। आप यहाँ देख सकते हैं: {url}"

# --- 3. AI Config ---
# अब आपको Secrets में सिर्फ API_KEY की ज़रूरत है
API_KEY = st.secrets["API_KEY"]
MODEL = ('gemini-2.5-flash-lite') 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराने संदेशों को दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Main Chat Logic ---
if user_input := st.chat_input("श्री हरि को कुछ पूछें..."):
    # यूजर का मैसेज दिखाना
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # हिस्ट्री तैयार करना
    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": msg["content"]}]})

    # API Payload (सिर्फ YouTube Tool के साथ)
    payload = {
        "contents": history,
        "tools": [{
            "function_declarations": [
                {
                    "name": "search_youtube",
                    "description": "यूट्यूब पर वीडियो, भजन या कथा खोजने के लिए",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}}
                    }
                }
            ]
        }]
    }

    try:
        response = requests.post(URL, json=payload, timeout=30)
        result = response.json()

        if 'candidates' in result:
            part = result['candidates'][0]['content']['parts'][0]
            
            # चेक करें कि AI काम करना चाहता है या सिर्फ बात
            if 'functionCall' in part:
                fn_name = part['functionCall']['name']
                args = part['functionCall']['args']
                
                if fn_name == "search_youtube":
                    with st.spinner("यूट्यूब पर खोज रहा हूँ..."):
                        ai_response = search_youtube(args.get('query', ''))
            else:
                ai_response = part.get('text', "क्षमा करें, मैं समझ नहीं पाया।")

            # जवाब दिखाना
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        else:
            st.error("AI से संपर्क नहीं हो पाया। कृपया अपनी API Key चेक करें।")

    except Exception as e:
        st.error(f"सिस्टम एरर: {e}")
