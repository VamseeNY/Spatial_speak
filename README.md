# CelestiaQ

An AI-powered Q&A chatbot trained on agricultural data from space-based research databases. This chatbot enables researchers to quickly extract insights from complex experiments conducted in space environments.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure API keys:
   - Edit `configure.py` with your AssemblyAI API key

3. Run the application:
   ```
   streamlit run app.py
   ```

## Features

- Natural language Q&A about space agriculture data
- Voice input capability with transcription
- Chat history management
- Session-based conversation tracking

## Project Structure

- `app.py`: Main Streamlit application
- `stt.py`: Speech-to-text functionality
- `chatbot_model.py`: Model integration
- `demo_notebook.py`: Model utilities
- `configure.py`: Configuration
- `llama stuff/`: Reference data for the LLM model