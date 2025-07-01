# Spatial Speak

**Spatial Speak** is an AI-powered question-answering system designed to assist scientists in querying and extracting insights from space agriculture-based experiments. Utilizing Retrieval-Augmented Generation (RAG), Spatial Speak enables efficient exploration of complex datasets.

![1741105611681](https://github.com/user-attachments/assets/9a22cd04-48bb-4883-b923-1b0cf8c796c7)

## Overview

The primary objective of Spatial Speak is to provide researchers with a tool to navigate and interpret data from spaceflight experiments involving plant biology. The system accesses datasets from NASA's [Open Science Data Repository (OSDR)](https://osdr.nasa.gov/bio/repo), focusing on studies related to plants under spaceflight and high-altitude conditions. These datasets include transcriptional profiles and other relevant biological data from experiments conducted aboard the International Space Station (ISS) and other spaceflight missions.

![1741105617009](https://github.com/user-attachments/assets/30e3909d-29d1-48b4-9f22-522ed1f5c4ee)

## Features

- **Natural Language Processing**: Allows users to pose questions in natural language and receive concise, relevant answers based on the underlying datasets.
- **Voice Input Capability**: Supports voice queries through integration with AssemblyAI's speech-to-text API, enabling hands-free interaction.
- **Session-Based Conversation Tracking**: Maintains context across multiple queries within a session for a coherent conversational experience.
- **Chat History Management**: Provides a record of previous interactions for reference and further analysis.

![1741105613977](https://github.com/user-attachments/assets/0e8e453b-69df-41e7-ae0b-680e29e34574)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd spatial_speak
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   - Open `configure.py`.
   - Insert your AssemblyAI API key to enable voice input functionality.

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main application script utilizing Streamlit for the user interface.
- `stt.py`: Handles speech-to-text conversion using AssemblyAI's API.
- `chatbot_model.py`: Contains functions and classes related to LLM integration and response generation.
- `demo_notebook.py`: Jupyter notebook demonstrating model utilities and sample interactions.
- `configure.py`: Stores configuration settings, including API keys.
- `llama_stuff/`: Directory containing reference data and resources for the LLM model.

## Data Source
Spatial Speak utilizes datasets from NASA's Open Science Data Repository (OSDR), specifically focusing on experiments involving plant root seedlings under spaceflight and high-altitude conditions. These studies provide valuable insights into plant biology in microgravity environments, contributing to the advancement of space agriculture research.
