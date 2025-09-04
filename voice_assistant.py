import speech_recognition as sr
from groq import Groq
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
from dotenv import load_dotenv

# === Load API keys from .env file ===
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# === Initialize clients ===
gpt_client = Groq(api_key=GROQ_API_KEY)
voice_client = ElevenLabs(api_key=ELEVEN_API_KEY)

# === SPEECH TO TEXT ===
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("📝 You said:", text)
        return text
    except sr.UnknownValueError:
        return "I couldn’t understand."
    except sr.RequestError:
        return "Speech service unavailable."

# === GROQ LLM RESPONSE ===
def ask_gpt(prompt):
    response = gpt_client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Choose the model you want
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    print("🤖 Assistant:", answer)
    return answer

# === ELEVEN LABS TTS ===
def speak(text):
    audio = voice_client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM" ,   #CHoose voice you want             
        text=text,
        model_id="eleven_multilingual_v2"
    )
    play(audio)

# === MAIN LOOP ===
if __name__ == "__main__":
    while True:
        command = listen()
        if not command:
            continue
        if "exit" in command.lower():
            print("👋 Exiting assistant...")
            break
        response = ask_gpt(command)
        speak(response)
