import streamlit as st
import assemblyai as aai
from configure import auth_key

# Set API key
aai.settings.api_key = auth_key

def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    
    if transcript.status == aai.TranscriptStatus.error:
        return f"Error: {transcript.error}"
    return transcript.text

# Streamlit UI
st.title("Audio Transcription App")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")
    
    # Save the file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("Transcribing... Please wait!")
    transcript_text = transcribe_audio(file_path)
    
    st.subheader("Transcription Output:")
    st.write(transcript_text)
