from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
import pyttsx3
import threading
import os
import tempfile
from gtts import gTTS
import pygame
import time
import json
from datetime import datetime
import re

app = Flask(__name__)

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Store conversation history
conversation_history = []

class RadheVoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        
        # Initialize text-to-speech engine
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
            
            # Get available voices and set Indian English/Hindi voice if available
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'hindi' in voice.name.lower() or 'indian' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except:
            self.engine = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("Processing speech...")
            # Try Hindi first, then English
            try:
                text = self.recognizer.recognize_google(audio, language="hi-IN")
                print(f"Hindi recognized: {text}")
            except:
                text = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"English recognized: {text}")
            
            return text
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def speak_pyttsx3(self, text):
        """Speak using pyttsx3 (offline)"""
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        return False
    
    def speak_gtts(self, text, lang='hi'):
        """Speak using Google TTS (online, better quality)"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_filename = temp_file.name
            temp_file.close()
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_filename)
            
            # Play audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            pygame.mixer.music.unload()
            os.unlink(temp_filename)
            
            return True
        except Exception as e:
            print(f"gTTS error: {e}")
            return False
    
    def speak(self, text, lang='hi'):
        """Speak text using available TTS method"""
        # Try gTTS first (better quality), fallback to pyttsx3
        if not self.speak_gtts(text, lang):
            self.speak_pyttsx3(text)
    
    def generate_response(self, user_input):
        """Generate response based on user input"""
        user_input_lower = user_input.lower()
        
        # Radhe Krishna themed responses
        responses = {
            'greeting': {
                'patterns': ['namaste', 'namaskar', 'hello', 'hi', 'hey', 'radhe', 'krishna', 'hare'],
                'response': "हरे कृष्ण! राधे राधे! मैं आपकी कैसे सहायता कर सकता हूँ?"
            },
            'how_are_you': {
                'patterns': ['how are you', 'kaise ho', 'kya haal', 'kaisa hai'],
                'response': "राधे राधे! मैं बिल्कुल ठीक हूँ, आपके साथ रहकर बहुत अच्छा लग रहा है। आप कैसे हैं?"
            },
            'name': {
                'patterns': ['what is your name', 'aap ka naam', 'kaun ho', 'who are you'],
                'response': "मैं राधे वॉयस असिस्टेंट हूँ, आपका अपना सहायक। राधे राधे!"
            },
            'time': {
                'patterns': ['time', 'samay', 'time kya hai', 'current time'],
                'response': f"अभी समय है {datetime.now().strftime('%I:%M %p')} बजे।"
            },
            'date': {
                'patterns': ['date', 'aaj ki date', 'konsi tarikh'],
                'response': f"आज {datetime.now().strftime('%d %B, %Y')} है।"
            },
            'weather': {
                'patterns': ['weather', 'mausam', 'temperature', 'mausam kaisa hai'],
                'response': "मुझे माफ करें, मैं अभी मौसम की जानकारी नहीं दे सकता। कृपया कोई दूसरा सवाल पूछें।"
            },
            'joke': {
                'patterns': ['joke', 'chutkula', 'hansaye', 'funny'],
                'response': "एक बार कृष्ण ने पूछा राधे से, 'तुम मेरी क्यों हो?' राधे मुस्कुराईं और बोलीं, 'क्योंकि तुम मेरे हो।' बस यही सच्ची हँसी है! हरे कृष्ण!"
            },
            'thanks': {
                'patterns': ['thanks', 'thank you', 'dhanyavad', 'shukriya'],
                'response': "आपका बहुत-बहुत धन्यवाद! राधे राधे! 🙏"
            },
            'goodbye': {
                'patterns': ['bye', 'goodbye', 'alvida', 'phir milenge'],
                'response': "राधे राधे! फिर मिलेंगे। हरे कृष्ण!"
            },
            'krishna': {
                'patterns': ['krishna', 'bhagwan', 'god', 'radha'],
                'response': "हरे कृष्ण हरे कृष्ण, कृष्ण कृष्ण हरे हरे। हरे राम हरे राम, राम राम हरे हरे। राधे राधे!"
            },
            'capabilities': {
                'patterns': ['what can you do', 'kya kar sakte ho', 'capabilities', 'help'],
                'response': "मैं आपकी इन चीज़ों में मदद कर सकता हूँ:\n• बातचीत करना\n• समय बताना\n• जोक्स सुनाना\n• कृष्ण भजन गाना\n• और भी बहुत कुछ!"
            }
        }
        
        # Check patterns for each response type
        for key, data in responses.items():
            for pattern in data['patterns']:
                if pattern in user_input_lower:
                    return data['response']
        
        # Default response for unrecognized input
        return f"राधे राधे! आपने कहा: '{user_input}'. मैं अभी इसे समझ नहीं पाया। कृपया कुछ और पूछें।"
    
    def process_voice_command(self):
        """Complete voice command processing pipeline"""
        try:
            # Listen for user input
            user_input = self.listen()
            
            if "No speech detected" in user_input:
                return {
                    'success': False,
                    'transcript': user_input,
                    'response': "मुझे कुछ सुनाई नहीं दिया। कृपया फिर से बोलें।",
                    'timestamp': datetime.now().isoformat()
                }
            elif "Could not understand" in user_input:
                return {
                    'success': False,
                    'transcript': user_input,
                    'response': "माफ करें, मैं समझ नहीं पाया। कृपया साफ बोलें।",
                    'timestamp': datetime.now().isoformat()
                }
            elif "Error" in user_input:
                return {
                    'success': False,
                    'transcript': user_input,
                    'response': "कोई तकनीकी समस्या आ गई है। कृपया पृष्ठ को रीफ्रेश करें।",
                    'timestamp': datetime.now().isoformat()
                }
            
            # Generate response
            response_text = self.generate_response(user_input)
            
            # Speak response (in a separate thread to not block)
            threading.Thread(target=self.speak, args=(response_text, 'hi')).start()
            
            # Return result
            return {
                'success': True,
                'transcript': user_input,
                'response': response_text,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'transcript': "Error occurred",
                'response': f"Error: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }

# Initialize assistant
assistant = RadheVoiceAssistant()

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    """API endpoint to listen and process voice"""
    result = assistant.process_voice_command()
    
    # Save to conversation history
    if result['success']:
        conversation_history.append({
            'user': result['transcript'],
            'assistant': result['response'],
            'timestamp': result['timestamp']
        })
    
    return jsonify(result)

@app.route('/speak', methods=['POST'])
def speak():
    """API endpoint to speak text"""
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', 'hi')
    
    if text:
        threading.Thread(target=assistant.speak, args=(text, lang)).start()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No text provided'})

@app.route('/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    return jsonify(conversation_history[-10:])  # Return last 10 messages

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
