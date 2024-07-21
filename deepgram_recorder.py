import streamlit as st
from streamlit_mic_recorder import mic_recorder
import io
import os
from deepgram import DeepgramClient, PrerecordedOptions


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# DEEPGRAM_API_KEY = "fa36c0989c4d2a4e447c204ae6889cc425370e21"

def transcribe_audio(audio_file):
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        options = PrerecordedOptions(
            model="nova-2-medical",
            language="en",
            intents=False, 
            smart_format=True, 
            punctuate=True, 
            paragraphs=True, 
            diarize=True, 
            filler_words=True, 
            sentiment=False, 
        )

        source = {'buffer': audio_file, 'mimetype': 'audio/wav'}
        response = deepgram.listen.rest.v("1").transcribe_file(source, options)

        return response

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

st.title("Audio Recorder and Transcription App")

# Record audio
audio_data = mic_recorder(
    start_prompt="Click to start recording",
    stop_prompt="Click to stop recording",
    just_once=False
)

if audio_data:
    # Create an in-memory file-like object
    audio_bytes = io.BytesIO(audio_data['bytes'])
    
    # Play the audio
    st.audio(audio_bytes, format="audio/wav")
    
    
    # Reset the buffer position to the beginning
    audio_bytes.seek(0)
    
    # Transcribe the recorded audio
    transcript = transcribe_audio(audio_bytes)

    if transcript:
        st.subheader("Transcription:")
        st.write(transcript['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript'])

    if st.button("Save Recording"):
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio_data['bytes'])
        st.success("Recording saved as recorded_audio.wav")

# Upload audio file option
st.subheader("Or upload an audio file")
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("Transcribe Uploaded Audio"):
        # Transcribe the uploaded audio
        transcript = transcribe_audio(uploaded_file)

        if transcript:
            st.subheader("Transcription:")
            st.write(transcript['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript'])