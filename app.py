import streamlit as st
import os
import torch
from transformers import VitsModel, AutoTokenizer
import tempfile
import time
import base64

# Import the modules from your existing code
from src.read_pdf import read_and_convert_page, total_pages
from src.txt_audio import process_long_text

# Set page config
st.set_page_config(
    page_title="PDF to Audio Converter",
    page_icon="🔊",
    layout="wide"
)

# Function to create an HTML audio player with autoplay option
def get_audio_player_html(audio_file_path, autoplay=False):
    audio_file = open(audio_file_path, "rb")
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    
    autoplay_attr = "autoplay" if autoplay else ""
    html_string = f'''
    <audio controls {autoplay_attr}>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        Your browser does not support the audio element.
    </audio>
    '''
    return html_string

def initialize_models():
    if 'model' not in st.session_state:
        with st.spinner("Loading TTS model... This may take a moment."):
            model_name = "facebook/mms-tts-eng"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = VitsModel.from_pretrained(model_name)
            
            # Set device (GPU if available)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            st.session_state.device_info = "🚀 Using GPU" if torch.cuda.is_available() else "💻 Using CPU"
            model = model.to(device)
            
            st.session_state.model = model
            st.session_state.tokenizer = tokenizer
            st.session_state.device = device

def main():
    st.title("PDF to Audio Converter")
    
    # Initialize models
    initialize_models()
    
    # Display device information
    st.sidebar.info(st.session_state.device_info)
    
    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_pdf_path = tmp_file.name
        
        try:
            # Get total pages
            pages = total_pages(temp_pdf_path)
            st.sidebar.success(f"PDF loaded successfully! Total pages: {pages}")
            
            # Page selection
            page_num = st.sidebar.number_input(
                "Select page to read", 
                min_value=0, 
                max_value=pages-1, 
                value=0,
                step=1
            )
            
            # Button to read and convert page
            if st.sidebar.button("Generate Audio"):
                with st.spinner("Reading page and generating audio..."):
                    # Read and convert page
                    _, content = read_and_convert_page(temp_pdf_path, page_num)
                    
                    # Display content
                    with st.expander("Page Content", expanded=True):
                        st.markdown(content)
                    
                    # Generate audio
                    output_file = f"page_{page_num}_{int(time.time())}.wav"
                    process_long_text(
                        content, 
                        st.session_state.model, 
                        st.session_state.tokenizer, 
                        st.session_state.device, 
                        output_file=output_file
                    )
                    
                    # Store audio file path in session state
                    st.session_state.audio_file = output_file
                    st.session_state.current_page = page_num
                
                # Display audio player after generation is complete
                st.subheader("Audio Player")
                st.markdown(get_audio_player_html(st.session_state.audio_file, autoplay=True), unsafe_allow_html=True)
                st.success(f"Audio for page {page_num + 1} generated successfully!")
                
                # Navigation buttons
                col1, col2, col3 = st.columns(3)
                
                # Previous page button
                if col1.button("⏮️ Previous Page") and page_num > 0:
                    st.rerun()
                
                # Replay button
                if col2.button("🔄 Replay"):
                    st.markdown(get_audio_player_html(st.session_state.audio_file, autoplay=True), unsafe_allow_html=True)
                
                # Next page button
                if col3.button("⏭️ Next Page") and page_num < pages - 1:
                    st.rerun()
            
            # Information about controls
            st.sidebar.markdown("---")
            st.sidebar.subheader("Instructions")
            st.sidebar.markdown("""
            1. Upload a PDF file
            2. Select a page number to read
            3. Click "Generate Audio" to convert text to speech
            4. Use navigation buttons to move between pages
            """)
                
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            
        finally:
            # Clean up the temporary file
            if 'temp_pdf_path' in locals():
                os.unlink(temp_pdf_path)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("PDF to Audio Converter")

if __name__ == "__main__":
    main()