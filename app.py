import streamlit as st
import requests
import sqlite3
import pandas as pd
import base64
from datetime import datetime
from gtts import gTTS
import streamlit.components.v1 as components

# --- 1. Database Logic ---
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
    c = conn.cursor()
    c.execute("INSERT INTO chat_history VALUES (?, ?, ?)", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, content))
    conn.commit()

# --- 2. Voice Output ---
def speak_text(text):
    try:
        clean_text = text.replace('*', '').replace('#', '')
        tts = gTTS(text=clean_text, lang='hi')
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- 3. UI Setup ---
st.set_page_config(page_title="Radhe AI Assistant", layout="wide")

st.markdown("""<style>.radhe-circle { width: 120px; height: 120px; border-radius: 50%; border: 3px solid #cc5500; display: flex; justify-content: center; align-items: center; margin: auto; color: #DAA520; font-weight: bold; text-align: center; font-size: 12px; }</style><div class="radhe-circle">OM NAMO<br>BAGVATE<br>VASUDEVAY</div>""", unsafe_allow_html=True)

# --- 4. Sidebar ---
with st.sidebar:
    st.title("📊 डैशबोर्ड")
    df_exp = pd.read_sql_query("SELECT item, amount FROM expenses", conn)
    if not df_exp.empty:
        st.bar_chart(df_exp.set_index('item'))
        st.metric("कुल खर्च", f"₹{df_exp['amount'].sum()}")
    st.divider()
    notes = conn.execute("SELECT content FROM notes ORDER BY date DESC LIMIT 3").fetchall()
    for n in notes: st.info(n[0])

# --- 5. Voice Input ---
st.write("### 🎙️ वॉइस कमांड")
voice_js = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'hi-IN';
function start() { recognition.start(); }
recognition.onresult = (e) => {
    const text = e.results[0][0].transcript;
    window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'voice_val', value: text}, '*');
};
</script>
<button onclick="start()" style="background: #cc5500; color: white; border: none; padding: 12px; border-radius: 25px; width: 100%; cursor: pointer;">🎤 माइक ऑन करें</button>
"""
components.html(voice_js, height=70)
voice_text = st.session_state.get('voice_val', "")

# --- 6. Chat Memory ---
if "messages" not in st.session_state:
    hist = conn.execute("SELECT role, content FROM chat_history ORDER BY timestamp ASC").fetchall()
    st.session_state.messages = [{"role": r, "content": c} for r, c in hist]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- 7. Main Logic ---
user_input = st.chat_input("यहाँ लिखें या माइक इस्तेमाल करें...")
final_input = voice_text if (voice_text and not user_input) else user_input

if final_input:
    if final_input == voice_text: st.session_state.voice_val = ""
    st.chat_message("user").markdown(final_input)
    st.session_state.messages.append({"role": "user", "content": final_input})
    save_chat("user", final_input)

    API_KEY = st.secrets["API_KEY"]
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

    # --- ERROR FIX: Logic to separate Tools vs Search ---
    task_keywords = ["खर्च", "नोट", "save", "expense", "youtube", "यूट्यूब", "लिखो", "बचाओ"]
    is_task = any(word in final_input.lower() for word in task_keywords)

    if is_task:
        tools = [{"function_declarations": [
            {"name": "track_expense", "description": "Save expense", "parameters": {"type": "object", "properties": {"item": {"type": "string"}, "amount": {"type": "number"}}}},
            {"name": "save_note", "description": "Save note", "parameters": {"type": "object", "properties": {"note": {"type": "string"}}}},
            {"name": "youtube_search", "description": "YouTube", "parameters": {"type": "object", "properties": {"q": {"type": "string"}}}}
        ]}]
    else:
        tools = [{"google_search": {}}]

    payload = {
        "contents": [{"role": m["role"]=="user" and "user" or "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages],
        "tools": tools
    }

    try:
        res = requests.post(URL, json=payload, timeout=30).json()
        if 'candidates' in res and len(res['candidates']) > 0:
            part = res['candidates'][0]['content']['parts'][0]
            
            if 'functionCall' in part:
                call = part['functionCall']
                if call['name'] == "track_expense":
                    conn.execute("INSERT INTO expenses VALUES (?, ?, ?)", (call['args']['item'], call['args']['amount'], datetime.now().strftime("%Y-%m-%d")))
                    conn.commit()
                    ai_res = f"₹{call['args']['amount']} नोट कर लिए गए हैं।"
                elif call['name'] == "save_note":
                    conn.execute("INSERT INTO notes VALUES (?, ?)", (call['args']['note'], datetime.now().strftime("%Y-%m-%d")))
                    conn.commit()
                    ai_res = "नोट सुरक्षित कर लिया गया है।"
                else:
                    ai_res = f"लिंक: https://www.youtube.com/results?search_query={call['args'].get('q', 'search')}"
            else:
                ai_res = part.get('text', "हरे कृष्ण!")
        else:
            ai_res = f"Error: {res.get('error', {}).get('message', 'No candidate')}"

        with st.chat_message("assistant"):
            st.markdown(ai_res)
            speak_text(ai_res)
        st.session_state.messages.append({"role": "assistant", "content": ai_res})
        save_chat("assistant", ai_res)
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
