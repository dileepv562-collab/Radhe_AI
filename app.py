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

# --- 2. Improved Voice Output (Fixed for Browsers) ---
def speak_text(text):
    try:
        if text:
            # फालतू सिम्बल्स हटाना ताकि आवाज़ साफ़ आए
            clean_text = text.replace('*', '').replace('#', '').replace('-', ' ')
            tts = gTTS(text=clean_text, lang='hi')
            tts.save("temp.mp3")
            
            with open("temp.mp3", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                
                # ब्राउज़र को फोर्स करने के लिए जावास्क्रिप्ट + ऑडियो टैग
                audio_html = f"""
                    <audio id="radhe-audio" autoplay>
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    <script>
                        var audio = document.getElementById('radhe-audio');
                        audio.play().catch(function(error) {{
                            console.log("Autoplay prevented. Needs user click.");
                        }});
                    </script>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Voice Error: {e}")

# --- 3. UI Setup ---
st.set_page_config(page_title="Radhe AI Assistant", layout="wide")

st.markdown("""
<style>
    .radhe-circle { width: 100px; height: 100px; border-radius: 50%; border: 2px solid #cc5500; 
                   display: flex; justify-content: center; align-items: center; margin: auto; 
                   color: #DAA520; font-weight: bold; text-align: center; font-size: 10px; }
    .stChatInput { position: fixed; bottom: 20px; }
</style>
<div class="radhe-circle">OM NAMO<br>BAGVATE<br>VASUDEVAY</div>
""", unsafe_allow_html=True)

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
voice_js = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'hi-IN';
function startMic() { recognition.start(); }
recognition.onresult = (e) => {
    const text = e.results[0][0].transcript;
    window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'voice_val', value: text}, '*');
};
</script>
<div style="position: fixed; bottom: 85px; right: 40px; z-index: 1000;">
    <button onclick="startMic()" style="background: #1e1e1e; color: #DAA520; border: 1px solid #444; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 20px;">🎙️</button>
</div>
"""
components.html(voice_js, height=0)
voice_text = st.session_state.get('voice_val', "")

# --- 6. Chat Memory ---
if "messages" not in st.session_state:
    hist = conn.execute("SELECT role, content FROM chat_history ORDER BY timestamp ASC LIMIT 20").fetchall()
    st.session_state.messages = [{"role": r, "content": c} for r, c in hist]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- 7. Main Logic ---
user_input = st.chat_input("श्री हरि को कुछ पूछें...")
final_input = voice_text if (voice_text and not user_input) else user_input

if final_input:
    if final_input == voice_text: st.session_state.voice_val = ""
    st.chat_message("user").markdown(final_input)
    st.session_state.messages.append({"role": "user", "content": final_input})
    save_chat("user", final_input)

    try:
        API_KEY = st.secrets["API_KEY"]
        MODEL = "gemini-2.5-flash-lite" # Stable model
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

        task_keywords = ["खर्च", "नोट", "save", "expense", "youtube", "लिखो", "बचाओ"]
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

        res = requests.post(URL, json=payload, timeout=30).json()
        
        if 'candidates' in res:
            part = res['candidates'][0]['content']['parts'][0]
            if 'functionCall' in part:
                call = part['functionCall']
                if call['name'] == "track_expense":
                    conn.execute("INSERT INTO expenses VALUES (?, ?, ?)", (call['args']['item'], call['args']['amount'], datetime.now().strftime("%Y-%m-%d")))
                    conn.commit()
                    ai_res = f"मैंने ₹{call['args']['amount']} का खर्च नोट कर लिया है।"
                elif call['name'] == "save_note":
                    conn.execute("INSERT INTO notes VALUES (?, ?)", (call['args']['note'], datetime.now().strftime("%Y-%m-%d")))
                    conn.commit()
                    ai_res = "आपका नोट सुरक्षित कर लिया गया है।"
                else:
                    ai_res = "यूट्यूब सर्च हो गया है।"
            else:
                ai_res = part.get('text', "हरे कृष्ण!")
        else:
            ai_res = "क्षमा करें, मैं अभी सुन नहीं पाया।"

        with st.chat_message("assistant"):
            st.markdown(ai_res)
            speak_text(ai_res) # यहाँ आवाज़ आएगी
        
        st.session_state.messages.append({"role": "assistant", "content": ai_res})
        save_chat("assistant", ai_res)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {e}")
