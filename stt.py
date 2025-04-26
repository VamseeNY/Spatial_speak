import sounddevice as sd
import numpy as np
import wave
import os
import requests
import time
import assemblyai as aai
from datetime import datetime
from configure import auth_key

# Set API key
aai.settings.api_key = auth_key

# Ensure audio directory exists
AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

def record_audio(duration=5, samplerate=16000, channels=1):
    """Records audio for a fixed duration and saves it."""
    filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    file_path = os.path.join(AUDIO_DIR, filename)

    print("🎤 Recording started...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype=np.int16)
    sd.wait()  # Blocking function (waits until recording is done)

    # Save the file
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    print(f"✅ Recording saved at: {file_path}")
    return file_path

def transcribe_audio(file_path):
    """Transcribes the given audio file using AssemblyAI API."""
    print(f"🔍 Transcribing file: {file_path}")  # Debugging

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return "Error: File not found"

    headers = {"authorization": auth_key}
    upload_url = "https://api.assemblyai.com/v2/upload"

    # Upload the audio file
    with open(file_path, "rb") as f:
        response = requests.post(upload_url, headers=headers, files={"file": f})

    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")  # Debugging
        return f"Error: Upload failed - {response.text}"

    audio_url = response.json()["upload_url"]
    print(f"✅ Upload successful: {audio_url}")

    # Request transcription
    transcript_request = {"audio_url": audio_url}
    transcribe_url = "https://api.assemblyai.com/v2/transcript"
    response = requests.post(transcribe_url, json=transcript_request, headers=headers)

    if response.status_code != 200:
        print(f"❌ Transcription request failed: {response.text}")  # Debugging
        return f"Error: Transcription request failed - {response.text}"

    transcript_id = response.json()["id"]
    print(f"📝 Transcription in progress: {transcript_id}")

    # Polling for transcription result
    import time  # Add this import

def transcribe_audio(file_path):
    """Transcribes audio using AssemblyAI API with timeout handling."""
    
    # Ensure the API key is set
    if not auth_key:
        return "Error: API key not found."

    headers = {'authorization': auth_key}
    # Debugging: Check API Key Usage
    masked_key = auth_key[:5] + "*" * (len(auth_key) - 5)
    print(f"🔍 Using API Key: {masked_key}")
    print(f"📡 Sending headers: {headers}")
    try:
        # Upload file
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://api.assemblyai.com/v2/upload', 
                headers=headers, 
                files={'file': f}
            )
        response.raise_for_status()  # 🔹 Ensure request is successful

        audio_url = response.json().get('upload_url')
        if not audio_url:
            return "Error: Upload failed. No URL returned."

        print(f"✅ File uploaded. URL: {audio_url}")

        # Request transcription
        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers=headers,
            json={'audio_url': audio_url}
        )
        transcript_response.raise_for_status()  # 🔹 Ensure request is successful

        transcript_id = transcript_response.json().get('id')
        if not transcript_id:
            return "Error: Failed to get transcript ID."

        print(f"🔄 Transcription requested. ID: {transcript_id}")

        # Poll for transcription result (timeout handling)
        max_retries = 30  # Limit retries (adjust based on API speed)
        retry_delay = 5  # Wait 5 seconds between retries

        for attempt in range(max_retries):
            result = requests.get(
                f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                headers=headers
            ).json()

            status = result.get('status', 'unknown')
            print(f"⏳ Checking status ({attempt + 1}/{max_retries}): {status}")

            if status == 'completed':
                print("✅ Transcription successful!")
                return result.get('text', "Error: No text returned.")
            elif status == 'failed':
                return "Error: Transcription failed."

            time.sleep(retry_delay)  # Wait before retrying

        return "Error: Transcription timeout reached."

    except requests.exceptions.RequestException as e:
        return f"Error: Network issue: {e}"
    except Exception as e:
        return f"Error: Unexpected issue: {e}"