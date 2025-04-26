from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import sounddevice as sd
import numpy as np
import wave
import os
from datetime import datetime
import assemblyai as aai

# Set API key (replace with your actual AssemblyAI key)
from configure import auth_key
aai.settings.api_key = auth_key

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change this to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store audio files
AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.post("/record/")
async def record_audio():
    """Records 5 seconds of audio and saves it as a WAV file."""
    samplerate = 44100
    duration = 5  # Record for 5 seconds

    print("Recording for 5 seconds...")  # Debugging
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype=np.int16)
    sd.wait()

    # Save the recording
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(AUDIO_DIR, f"recording_{timestamp}.wav")

    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    return {"message": "Recording saved", "file_path": file_path}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribes an uploaded audio file and returns text."""
    file_location = f"{AUDIO_DIR}/{file.filename}"
    
    # Save the uploaded file
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio using AssemblyAI
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_location)

    # Delete the audio file after transcription
    os.remove(file_location)

    if transcript.status == aai.TranscriptStatus.error:
        return {"error": transcript.error}
    
    return {"transcription": transcript.text}

@app.get("/")
def home():
    return {"message": "Speech-to-Text API is running!"}
