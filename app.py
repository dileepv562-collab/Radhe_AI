import requests
import json
import os
import time

# --- Setup ---
API_KEY = "AIzaSyCZfPk0w1mX4cTkzVOKjkGaD70mve2zW_M"
MODEL = "gemini-3-flash-preview" 
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def show_divine_circle():
    """Divine Circle: Om Namo Bhagavate Vasudevaya"""
    # Gold color code: \033[1;33m
    circle = """
    \033[1;33m
               .---.
            .'       '.
           /   OM NAMO  \\
          |  BHAGAVATE   |
           \ VASUDEVAYA /
            '.       .'
               '---'
    \033[0m"""
    print(circle)
    print("\033[1;36mॐ नमो भगवते वासुदेवाय\033[0m\n")

def speak_lyra(text):
    """Voice fix for Failed transaction error"""
    try:
        os.system(f'am start -a android.intent.action.TTS_SERVICE -e text "{text}" > /dev/null 2>&1 &')
    except:
        pass

def radhe_ai_final_v4():
    os.system('clear')
    show_divine_circle()
    print("-" * 40)
    print("   RADHE AI: GEMINI 3 + LYRA (STABLE)   ")
    print("-" * 40)
    print("Radhe-Radhe Dilip Ji!]\n")
    
    while True:
        try:
            user_input = input("\033[1;32mDilip Ji:\033[0m ")
            if user_input.lower() in ['exit', 'stop', 'band']: break

            payload = {
                "contents": [{"parts": [{"text": f"Your name is Radhe AI. Use Lyra voice style. Talking to Dilip. Start with Radhe Radhe. Hindi: {user_input}"}]}]
            }
            
            headers = {'Content-Type': 'application/json'}
            
            # Read timeout fix: 10 se badha kar 30 kiya
            response = requests.post(URL, headers=headers, json=payload, timeout=30)
            result = response.json()
            
            if 'candidates' in result:
                ai_text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"\n\033[1;36mRadhe AI (Lyra):\033[0m {ai_text}\n")
                speak_lyra(ai_text)
            elif 'error' in result:
                print(f"\n[AI Error]: {result['error']['message']}")
                
        except requests.exceptions.ReadTimeout:
            # Time out error handling
            print("\n\033[1;31m[Wait]: Internet thoda slow hai, main dhyan laga raha hoon...\033[0m")
            time.sleep(1)
        except Exception as e:
            print(f"\n[System Error]: {e}")

if __name__ == "__main__":
    radhe_ai_final_v4()
    
