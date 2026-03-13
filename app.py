import streamlit as st
import requests
import sqlite3
import pandas as pd
from datetime import datetime

# --- 1. Database Setup ---
def init_db():
    conn = sqlite3.connect('radhe_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (timestamp TEXT, role TEXT, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (item TEXT, amount REAL, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes (content TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def save_chat(role, content):
    conn = sqlite3.connect('radhe_memory.db')
    conn.cursor().execute("INSERT INTO chat_history VALUES (?, ?, ?)", 
                          (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, content))
    conn.commit()
    conn.close()

def save_expense(item, amount):
    conn = sqlite3.connect('radhe_memory.db')
    conn.cursor().execute("INSERT INTO expenses VALUES (?, ?, ?)", 
                          (item, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def save_note(note_content):
    conn = sqlite3.connect('radhe_memory.db')
    conn.cursor().execute("INSERT INTO notes VALUES (?, ?)", 
                          (note_content, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
    return f"नोट सुरक्षित कर लिया गया है: '{note_content}'"

init_db()

# --- 2. UI Setup ---
st.set_page_config(page_title="Radhe AI", page_icon="🕉️", layout="wide")

st.markdown("""
<style>
    .radhe-circle-container { display: flex; justify-content: center; align-items: center; margin: 10px 0; }
    .radhe-circle-border { width: 180px; height: 180px; border-radius: 50%; border: 4px solid #cc5500; display: flex; justify-content: center; align-items: center; }
    .radhe-circle-text { text-align: center; color: #DAA520; font-weight: bold; font-size: 1em; }
</style>
<div class="radhe-circle-container">
    <div class="radhe-circle-border"><div class="radhe-circle-text">OM NAMO<br>BAGVATE<br>VASUDEVAY</div></div>
</div>
""", unsafe_allow_html=True)

# --- 3. Sidebar (Charts & Notes) ---
with st.sidebar:
    st.title("📊 डैशबोर्ड")
    
    # Expense Chart
    conn = sqlite3.connect('radhe_memory.db')
    df_exp = pd.read_sql_query("SELECT item, amount FROM expenses", conn)
    if not df_exp.empty:
        st.subheader("खर्चों का विश्लेषण")
        st.bar_chart(df_exp.set_index('item'))
        st.write(f"**कुल खर्च: ₹{df_exp['amount'].sum()}**")
    
    # Notes Display
    st.divider()
    st.subheader("📝 आपके नोट्स")
    notes = conn.execute("SELECT content FROM notes ORDER BY date DESC LIMIT 5").fetchall()
    for n in notes:
        st.info(n[0])
    conn.close()

# --- 4. AI & Tools Setup ---
API_KEY = st.secrets["API_KEY"]
MODEL = ('gemini-2.5-flash-lite') 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    conn = sqlite3.connect('radhe_memory.db')
    history = conn.execute("SELECT role, content FROM chat_history ORDER BY timestamp ASC").fetchall()
    st.session_state.messages = [{"role": r, "content": c} for r, c in history]
    conn.close()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. Main Logic ---
if user_input := st.chat_input("श्री हरि को कुछ पूछें..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_chat("user", user_input)

    history = [{"role": m["role"]=="user" and "user" or "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages]

    payload = {
        "contents": history,
        "tools": [
            {"google_search": {}}, 
            {"function_declarations": [
                {"name": "search_youtube", "description": "Search YouTube", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}},
                {"name": "track_expense", "description": "Record expense", "parameters": {"type": "object", "properties": {"item": {"type": "string"}, "amount": {"type": "number"}}}},
                {"name": "save_note", "description": "Save a personal note", "parameters": {"type": "object", "properties": {"note_content": {"type": "string"}}}}
            ]}
        ]
    }

    try:
        res = requests.post(URL, json=payload).json()
        if 'candidates' in res:
            part = res['candidates'][0]['content']['parts'][0]
            
            if 'functionCall' in part:
                call = part['functionCall']
                if call['name'] == "search_youtube":
                    ai_response = f"यूट्यूब लिंक: https://www.youtube.com/results?search_query={call['args']['query']}"
                elif call['name'] == "track_expense":
                    save_expense(call['args']['item'], call['args']['amount'])
                    ai_response = f"₹{call['args']['amount']} '{call['args']['item']}' के लिए नोट कर लिए हैं।"
                elif call['name'] == "save_note":
                    ai_response = save_note(call['args']['note_content'])
            else:
                ai_response = part.get('text', "समझ नहीं आया।")

            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            save_chat("assistant", ai_response)
            st.rerun() # UI/Sidebar अपडेट करने के लिए
    except Exception as e:
        st.error(f"Error: {e}")
