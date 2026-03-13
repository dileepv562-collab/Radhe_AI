import streamlit as st
import requests

# --- 1. Page & UI Setup ---
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

st.markdown("""
<style>
    .radhe-circle-container { display: flex; justify-content: center; align-items: center; margin: 20px 0; }
    .radhe-circle-border { width: 220px; height: 220px; border-radius: 50%; border: 4px solid #cc5500; display: flex; justify-content: center; align-items: center; }
    .radhe-circle-text { text-align: center; color: #DAA520; font-weight: bold; font-size: 1.2em; }
</style>
<div class="radhe-circle-container">
    <div class="radhe-circle-border"><div class="radhe-circle-text">OM NAMO<br>BAGVATE<br>VASUDEVAY</div></div>
</div>
""", unsafe_allow_html=True)

st.title("🕉️ Radhe AI: आपका सहायक")

# --- 2. Functions (The Tools) ---

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    return f"मैंने यूट्यूब पर '{query}' खोजा है। यहाँ देखें: {url}"

def track_expense(item, amount):
    if "expenses" not in st.session_state:
        st.session_state.expenses = []
    
    st.session_state.expenses.append({"item": item, "amount": amount})
    total = sum(ex['amount'] for ex in st.session_state.expenses)
    return f"ठीक है, मैंने '{item}' के लिए ₹{amount} नोट कर लिए हैं। अब तक का कुल खर्च ₹{total} है।"

# --- 3. AI Config ---
API_KEY = st.secrets["API_KEY"]
MODEL = "gemini-2.0-flash-exp" # आपका पसंदीदा नया मॉडल
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Main Chat Logic ---
if user_input := st.chat_input("श्री हरि को कुछ पूछें..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": msg["content"]}]})

    payload = {
        "contents": history,
        "tools": [{
            "function_declarations": [
                {
                    "name": "search_youtube",
                    "description": "YouTube search for videos",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
                },
                {
                    "name": "track_expense",
                    "description": "Track money spent on items",
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "item": {"type": "string", "description": "चीज़ का नाम"},
                            "amount": {"type": "number", "description": "रुपये"}
                        }
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
            
            if 'functionCall' in part:
                fn = part['functionCall']
                if fn['name'] == "search_youtube":
                    ai_response = search_youtube(fn['args']['query'])
                elif fn['name'] == "track_expense":
                    ai_response = track_expense(fn['args']['item'], fn['args']['amount'])
            else:
                ai_response = part.get('text', "क्षमा करें, मैं समझ नहीं पाया।")
            
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
    except Exception as e:
        st.error(f"Error: {e}")

# साइडबार में खर्चों की लिस्ट दिखाना
if "expenses" in st.session_state and st.session_state.expenses:
    with st.sidebar:
        st.header("📉 आपका हिसाब-किताब")
        for ex in st.session_state.expenses:
            st.write(f"- {ex['item']}: ₹{ex['amount']}")
        st.divider()
        st.write(f"**कुल खर्च: ₹{sum(ex['amount'] for ex in st.session_state.expenses)}**")
