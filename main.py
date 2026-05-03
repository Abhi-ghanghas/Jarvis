# 📦 Imports
import speech_recognition as sr
import webbrowser
import pyttsx3
import openai
import musicLibrary
from datetime import datetime

# 🔐 Env setup
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🎙️ Text-to-Speech
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# 🌐 AI Availability Flag
AI_AVAILABLE = True

# 🤖 AI Function
def ask_ai(prompt):
    global AI_AVAILABLE

    if not AI_AVAILABLE:
        return offline_response(prompt)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart voice assistant named Jarvis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        print("AI Error:", e)
        AI_AVAILABLE = False
        return "I am offline now but still listening."

# 🧠 Offline Smart Replies
def offline_response(command):
    command = command.lower()

    if "time" in command:
        return f"The time is {datetime.now().strftime('%H:%M')}"

    elif "date" in command:
        return f"Today's date is {datetime.now().strftime('%d %B %Y')}"

    elif "hello" in command or "hi" in command:
        return "Hello! I am offline but still here."

    elif "your name" in command:
        return "I am Jarvis, running in offline mode."

    elif "how are you" in command:
        return "I am functioning well, even without internet."

    else:
        return "I am offline now but still listening."

# 🧠 Command Processor
def processCommand(command):
    command = command.lower()

    # 🌐 Websites
    if "open google" in command:
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")

    # 🎵 Smart Music
    elif "play" in command:
        song = command.replace("play", "").strip()

        if song == "":
            if AI_AVAILABLE:
                song = ask_ai("Suggest a trending song")
            else:
                song = "random song"

        speak(f"Playing {song}")
        musicLibrary.play_song(song)

    # ❌ Exit
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    # 🤖 AI / Offline fallback
    else:
        response = ask_ai(command)
        speak(response)

# 🎤 MAIN LOOP
if __name__ == "__main__":
    speak("Initializing AI Jarvis...")
    recognizer = sr.Recognizer()

    while True:
        try:
            # Wake word
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)

            if "jarvis" in word.lower():
                speak("Yes?")

                # Command listening
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except Exception as e:
            print("Error:", e)