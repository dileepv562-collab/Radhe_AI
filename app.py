import streamlit as st
import requests
import smtplib
import webbrowser
from email.mime.text import MIMEText

# --- Setup ---
st.set_page_config(page_title="Radhe AI", page_icon="🕉️")

# --- UI Circle Feature ---
st.markdown("""
<style>
    .radhe-circle-container { display: flex; justify-content: center; align-items: center; margin: 20px 0; }
    .radhe-circle-border { width: 250px; height: 250px; border-radius: 50%; border: 4px solid #cc5500; display: flex; justify-content: center; align-items: center; }
    .radhe-circle-text { text-align: center; color: #DAA520; font-weight: bold; font-size: 1.2em; }
</style>
<div class="radhe-circle-container">
    <div class="radhe-circle-border">
        <div class="radhe-circle-text">OM NAMO<br>BAGVATE<br>VASUDEVAY</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🕉️ Radhe AI: आपका डिजिटल सहायक")

# --- Functions (The 'Work' part) ---

def search_youtube(query):
    """यूट्यूब पर वीडियो खोजने के लिए"""
    url = f"https://www.youtube.com/results?search_query={query}"
    # नोट: Streamlit क्लाउड पर ब्राउज़र सीधा नहीं खुलता, हम लिंक देंगे
    return f"मैंने यूट्यूब पर '{query}' के लिए खोज की है। यहाँ देखें: {url}"

def send_email(receiver_email, subject, message):
    """ईमेल भेजने के लिए"""
    sender_email = st.secrets["MY_EMAIL"] # आपकी ईमेल आईडी
    password = st.secrets["EMAIL_PASSWORD"] # आपका App Password
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return "ईमेल सफलतापूर्वक भेज दिया गया है।"
    except Exception as e:
        return f"ईमेल भेजने में त्रुटि: {str(e)}"

# --- AI Logic ---
API_KEY = st.secrets["API_KEY"]
MODEL = "('gemini-2.5-flash-lite')" # Function calling के लिए flash मॉडल बेस्ट है
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("श्री हरि को कुछ पूछें..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare Context
    history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Tools Definition
    payload = {
        "contents": history,
        "tools": [{
            "function_declarations": [
                {
                    "name": "search_youtube",
                    "description": "यूट्यूब पर वीडियो या भजन खोजने के लिए",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
                },
                {
                    "name": "send_email",
                    "description": "ईमेल भेजने के लिए",
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "receiver_email": {"type": "string"},
                            "subject": {"type": "string"},
                            "message": {"type": "string"}
                        }
                    }
                }
            ]
        }]
    }

    try:
        response = requests.post(URL, json=payload).json()
        
        # यहाँ AI तय करेगा कि उसे 'बात' करनी है या 'काम' (Function call)
        if 'candidates' in response:
            part = response['candidates'][0]['content']['parts'][0]
            
            if 'functionCall' in part:
                # अगर AI काम करना चाहता है
                fn_name = part['functionCall']['name']
                args = part['functionCall']['args']
                
                if fn_name == "search_youtube":
                    res = search_youtube(args['query'])
                elif fn_name == "send_email":
                    res = send_email(args['receiver_email'], args['subject'], args['message'])
                
                ai_output = res
            else:
                ai_output = part['text']
            
            with st.chat_message("assistant"):
                st.markdown(ai_output)
            st.session_state.messages.append({"role": "assistant", "content": ai_output})

    except Exception as e:
        st.error(f"त्रुटि: {e}")
