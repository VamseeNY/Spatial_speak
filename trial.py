import streamlit as st
import assemblyai as aai
import websocket
import json
import threading
import pyaudio
import time
from configure import auth_key

# Set API key
aai.settings.api_key = auth_key

# Streaming settings
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# WebSocket URL
ws_url = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# Global variables
ws = None
st.session_state.recording = False
st.session_state.transcribed_text = ""

# Streamlit UI
st.title("Real-time Audio Transcription App")

transcription = st.empty()

def on_message(ws, message):
    response = json.loads(message)
    if "text" in response:
        st.session_state.transcribed_text = response["text"]
        transcription.text(st.session_state.transcribed_text)

def on_error(ws, error):
    st.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    st.info("WebSocket closed")
    transcription.text("Final Transcription:\n" + st.session_state.transcribed_text)

def on_open(ws):
    def run():
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK_SIZE)
        try:
            while st.session_state.recording:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            st.error(f"Error streaming audio: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            time.sleep(1)  # Allow last transcription to process
            ws.close()
    threading.Thread(target=run, daemon=True).start()

def start_recording():
    if st.session_state.recording:
        st.warning("Already recording!")
        return
    st.session_state.recording = True
    st.session_state.transcribed_text = ""
    st.write("Recording started...")
    headers = {"authorization": auth_key}
    global ws
    ws = websocket.WebSocketApp(ws_url, header=headers, on_message=on_message,
                                on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    threading.Thread(target=ws.run_forever, daemon=True).start()

def stop_recording():
    if not st.session_state.recording:
        st.warning("Recording is not active!")
        return
    st.session_state.recording = False
    st.write("Recording stopped.")
    if ws:
        ws.close()

st.write("Click the button to start or stop recording.")
if st.button("Start Recording"):
    start_recording()
if st.button("Stop Recording"):
    stop_recording()
