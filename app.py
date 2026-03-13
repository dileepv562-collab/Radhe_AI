import streamlit as st
import requests
import sqlite3
import pandas as pd
import base64
from datetime import datetime
from gtts import gTTS
import streamlit.components.v1 as components

# --- 1. Database & Memory Setup ---
def init_db():
    conn = sqlite3.connect('radhe_advanced.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (timestamp TEXT, role TEXT, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (item TEXT, amount REAL, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes (content TEXT, date TEXT)''')
    conn.commit()
    return conn

conn = init_db()

def save_chat(role, content):
    conn.cursor().execute("INSERT INTO chat_history VALUES (?, ?, ?)", 
                          (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, content))
    conn.commit()

# --- 2. Voice Output (Text-to-Speech) ---
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
            st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass

# --- 3. UI Setup ---
st.set_page_config(page_title="Radhe AI Voice Assistant", layout="wide")

st.markdown("""<style>.radhe-circle { width: 150px; height: 150px; border-radius: 50%; border: 4px solid #cc5500; display: flex; justify-content: center; align-items: center; margin: auto; color: #DAA520; font-weight: bold; text-align: center; }</style>
<div class="radhe-circle">OM NAMO<br>BAGVATE<br>VASUDEVAY</div>""", unsafe_allow_html=True)

# --- 4. Sidebar (Dashboard) ---
with st.sidebar:
    st.title("📊 डैशबोर्ड")
    df_exp = pd.read_sql_query("SELECT item, amount FROM expenses", conn)
    if not df_exp.empty:
        st.subheader("खर्चों का ग्राफ")
        st.bar_chart(df_exp.set_index('item'))
        st.metric("कुल खर्च", f"₹{df_exp['amount'].sum()}")
    
    st.divider()
    st.subheader("📝 हालिया नोट्स")
    notes = conn.execute("SELECT content FROM notes ORDER BY date DESC LIMIT 3").fetchall()
    for n in notes: st.info(n[0])

# --- 5. Voice Input (Speech-to-Text) ---
st.write("### 🎙️ बोलकर पूछें")
voice_js = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'hi-IN';
function start() { recognition.start(); }
recognition.onresult = (e) => {
    const text = e.results[0][0].transcript;
    parent.postMessage({type: 'streamlit:set_widget_value', key: 'voice_val', value: text}, '*');
};
</script>
<button onclick="start()" style="background: #cc5500; color: white; border: none; padding: 10px 20px; border-radius: 20px; width: 100%;">🎤 माइक ऑन करें</button>
"""
components.html(voice_js, height=50)
voice_text = st.session_state.get('voice_val', "")

# --- 6. Chat System ---
if "messages" not in st.session_state:
    hist = conn.execute("SELECT role, content FROM chat_history ORDER BY timestamp ASC LIMIT 20").fetchall()
    st.session_state.messages = [{"role": r, "content": c} for r, c in hist]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- 7. Logic & Tools ---
user_input = st.chat_input("यहाँ लिखें या माइक इस्तेमाल करें...")
final_input = voice_text if voice_text and not user_input else user_input

if final_input:
    st.chat_message("user").markdown(final_input)
    st.session_state.messages.append({"role": "user", "content": final_input})
    save_chat("user", final_input)

    API_KEY = st.secrets["API_KEY"]
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"role": m["role"]=="user" and "user" or "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages],
        "tools": [{"google_search": {}}, {"function_declarations": [
            {"name": "track_expense", "description": "Save expense", "parameters": {"type": "object", "properties": {"item": {"type": "string"}, "amount": {"type": "number"}}}},
            {"name": "save_note", "description": "Save note", "parameters": {"type": "object", "properties": {"note": {"type": "string"}}}},
            {"name": "youtube", "description": "YouTube", "parameters": {"type": "object", "properties": {"q": {"type": "string"}}}}
        ]}]
    }

    try:
        res = requests.post(URL, json=payload).json()
        part = res['candidates'][0]['content']['parts'][0]
        
        if 'functionCall' in part:
            call = part['functionCall']
            if call['name'] == "track_expense":
                conn.execute("INSERT INTO expenses VALUES (?, ?, ?)", (call['args']['item'], call['args']['amount'], datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                ai_res = f"₹{call['args']['amount']} बचा लिए गए हैं।"
            elif call['name'] == "save_note":
                conn.execute("INSERT INTO notes VALUES (?, ?)", (call['args']['note'], datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                ai_res = "नोट लिख लिया गया है।"
            else:
                ai_res = f"यूट्यूब लिंक: https://www.youtube.com/results?search_query={call['args']['q']}"
        else:
            ai_res = part.get('text', "हरे कृष्ण!")

        with st.chat_message("assistant"):
            st.markdown(ai_res)
            speak_text(ai_res)
        st.session_state.messages.append({"role": "assistant", "content": ai_res})
        save_chat("assistant", ai_res)
        if voice_text: st.session_state.voice_val = "" # Clear voice
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
