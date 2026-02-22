# Step 1: Run this once in Colab
!pip install -q requests

import requests
import json
from google.colab import output
from IPython.display import Javascript

# --- SETUP ---
API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"
# Gemini 3 Flash Preview - Fast & Smart
MODEL = "gemini-3-flash-preview" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def show_divine_circle():
    """Divine Circle: Om Namo Bhagavate Vasudevaya"""
    circle = r"""
               .---.
            .'       '.
           /   OM NAMO  \
          |  BHAGAVATE   |
           \ VASUDEVAYA /
            '.       .'
               '---'
    """
    print("\033[1;33m" + circle + "\033[0m") 
    print("\033[1;36mॐ नमो भगवते वासुदेवाय\033[0m\n")

def colab_speak(text):
    """Voice output"""
    display(Javascript(f'window.speechSynthesis.speak(new SpeechSynthesisUtterance("{text}"));'))

def start_radhe_ai_2026():
    show_divine_circle()
    print("-" * 40)
    print("      RADHE AI: 2026 LIVE SEARCH MODE      ")
    print("-" * 40)
    print("Radhe-Radhe Dilip Ji!]\n")
    
    colab_speak("राधे राधे दिलीप जी! मैं 2026 के लाइव डेटा के साथ तैयार हूँ।")
    
    while True:
        try:
            user_input = input("Dilip Ji: ")
            if user_input.lower() in ['exit', 'stop', 'band']: break

            # 2026 Live Data Enable करने वाला Payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Current date is Feb 2026. Use Google Search to provide live updates for Dilip: {user_input}"
                    }]
                }],
                "tools": [{"google_search_retrieval": {}}] # Yeh line 2024 ke data ko 2026 me badal degi
            }
            
            response = requests.post(URL, headers={'Content-Type': 'application/json'}, json=payload, timeout=30)
            result = response.json()
            
            if 'candidates' in result:
                ai_text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"\nRadhe AI: {ai_text}\n" + "-"*20)
                colab_speak(ai_text)
            elif 'error' in result:
                print(f"\n[Error]: {result['error']['message']}")
                
        except Exception as e:
            print(f"\n[System Error]: {e}")

if __name__ == "__main__":
    start_radhe_ai_2026()
