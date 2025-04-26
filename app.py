import streamlit as st
import os
from datetime import datetime
from stt import record_audio, transcribe_audio
from chatbot_model import get_response  # Replace with your actual model integration

# Directory to save audio files
AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = []  # Stores past conversations
if "text_input" not in st.session_state:
    st.session_state.text_input = ""  # Store user input
if "recording_in_progress" not in st.session_state:
    st.session_state.recording_in_progress = False  # Prevent double recording

st.set_page_config(page_title="Spatial Speak", layout="wide")

# Sidebar for past conversations
st.sidebar.title("Past Conversations")
if st.sidebar.button("Start New Conversation"):
    if st.session_state.chat_history:
        st.session_state.conversations.append(st.session_state.chat_history.copy())
    st.session_state.chat_history = []  # Clear current chat
    st.session_state.recording_in_progress = False  # Reset recording state
    st.rerun()

for i, conv in enumerate(st.session_state.conversations):
    with st.sidebar.expander(f"Conversation {i+1}"):
        for role, message in conv:
            st.write(f"**{role}:** {message}")

st.title("Spatial Speak")

# Scrollable conversation history
chat_container = st.container()
with chat_container:
    for role, message in st.session_state.chat_history:
        st.markdown(f"**{role}:** {message}")

# Function to handle text input submission
def handle_submit():
    user_text = st.session_state.text_input.strip()
    if user_text:  # Only process non-empty input
        st.session_state.chat_history.append(("User", user_text))

        # Get model response
        bot_response = get_response(user_text)
        st.session_state.chat_history.append(("Bot", bot_response))

    # Clear text input
    st.session_state.text_input = ""

# Input box with Enter key submission
st.text_input(
    "Type your query here and press Enter...",
    key="text_input",
    on_change=handle_submit
)

# **Audio Recording Section**
def record_and_transcribe():
    """Records audio, saves it, transcribes it, and updates chat."""
    if st.session_state.recording_in_progress:
        print("⚠️ Recording already in progress, skipping...")
        return  # Prevent duplicate recordings
    
    st.session_state.recording_in_progress = True  # Lock recording
    print("🎤 Recording started...")

    st.write("🎤 **Recording... Please wait**")
    
    file_path = record_audio(duration=5)

    if not file_path:  # Check if record_audio() returned None
        print("❌ record_audio() returned None!")
        st.write("⚠️ Recording failed. Try again.")
        st.session_state.recording_in_progress = False
        return

    if not os.path.exists(file_path):  # Double-check file existence
        print(f"❌ File does not exist at path: {file_path}")
        st.write("⚠️ Recording failed. Try again.")
        st.session_state.recording_in_progress = False
        return

    print(f"✅ Recording saved at: {file_path}")
    st.write(f"✅ **Recording saved: {file_path}**")
    st.write("🔄 **Transcribing...**")

    # **DEBUG: Print the file path before transcription**
    print(f"📂 File exists: {os.path.exists(file_path)} | Path: {file_path}")

    # Transcribe audio
    print("🔍 Calling transcribe_audio()...")
    try:
        transcript = transcribe_audio(file_path)
        print(f"✅ Transcription result: {transcript}")
    except Exception as e:
        print(f"❌ ERROR during transcription: {str(e)}")
        st.write(f"⚠️ **Transcription failed:** {str(e)}")
        st.session_state.recording_in_progress = False
        return  

    if not transcript or transcript.startswith("Error"):
        print(f"❌ Transcription failed: {transcript}")
        st.write(f"⚠️ **Transcription failed:** {transcript}")
        st.session_state.recording_in_progress = False
        return  

    # **Add transcript to chat history**
    st.session_state.chat_history.append(("User", transcript))

    # Get model response
    bot_response = get_response(transcript)
    st.session_state.chat_history.append(("Bot", bot_response))

    # Unlock recording for next use
    st.session_state.recording_in_progress = False
    print("✅ Recording & transcription complete.")
    st.rerun()


# Button to trigger recording
if st.button("🎤 Record & Transcribe", key="record_button") and not st.session_state.recording_in_progress:
    record_and_transcribe()
