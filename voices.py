from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Init client
client = ElevenLabs(api_key=ELEVEN_API_KEY)

# Get voices
voices = client.voices.get_all()

print("Available voices in your ElevenLabs account:")
for v in voices.voices:
    print(f"- {v.name} (voice_id: {v.voice_id})")
