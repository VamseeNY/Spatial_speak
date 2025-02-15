import streamlit as st
import openai
import sounddevice as sd
import numpy as np
import queue
import tempfile
import wave
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API key and validate
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key is missing! Set OPENAI_API_KEY in .env or environment variables.")
    st.stop()

openai.api_key = api_key

# Streamlit UI
st.title("Real-time Speech to Text with Whisper API")
st.write("Click 'Start Recording' and speak. The Whisper API will transcribe in real-time!")

# Audio Recording Configuration
q = queue.Queue()
def callback(indata, frames, time, status):
    if status:
        st.error(status)
    q.put(indata.copy())

# Record Audio
def record_audio(duration=5, samplerate=44100, channels=1):
    q.queue.clear()  # Clear previous data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        filename = temp_audio.name
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                st.write("Recording... Speak now!")
                for _ in range(0, int(samplerate / 1024 * duration)):
                    wf.writeframes(q.get())
        return filename

if st.button("Start Recording"):
    audio_file = record_audio()
    st.write("Processing...")
    
    # Send audio file to Whisper API
    with open(audio_file, "rb") as audio:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="json"
        )
    
    st.write("### Transcribed Text:")
    st.write(response["text"])
