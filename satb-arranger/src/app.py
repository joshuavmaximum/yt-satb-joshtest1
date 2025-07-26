"""Streamlit web interface for SATB Arranger tool."""

import streamlit as st
import tempfile
import shutil
from pathlib import Path
import base64
import os

from youtube_downloader import YouTubeDownloader
from stem_separator import StemSeparator
from arranger import SATBArranger
from midi_generator import MIDIGenerator


st.set_page_config(
    page_title="SATB Arranger",
    page_icon="🎵",
    layout="wide"
)


def get_download_link(file_path, text):
    """Generate a download link for a file."""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    filename = Path(file_path).name
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'


def main():
    st.title("🎵 SATB Arranger Tool")
    st.markdown("Create four-part SATB vocal arrangements from YouTube videos")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        arrangement_style = st.selectbox(
            "Arrangement Style",
            ["hymn", "jazz", "classical"],
            help="Choose the style of arrangement"
        )
        
        num_stems = st.radio(
            "Stem Separation Quality",
            [2, 4, 5],
            format_func=lambda x: {
                2: "Fast (vocals/accompaniment)",
                4: "Better (vocals/drums/bass/other)",
                5: "Best (vocals/drums/bass/piano/other)"
            }[x],
            help="More stems = better separation but slower processing"
        )
        
        keep_audio = st.checkbox("Keep audio files", value=False)
        
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Input")
        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste the URL of the YouTube video you want to arrange"
        )
        
        process_button = st.button("Create Arrangement", type="primary", use_container_width=True)
        
    with col2:
        st.header("How it works")
        st.markdown("""
        1. **Download** audio from YouTube
        2. **Separate** vocals using AI (Spleeter)
        3. **Analyze** melody and harmony
        4. **Create** four-part arrangement
        5. **Export** individual MIDI files
        """)
        
    # Process when button clicked
    if process_button and youtube_url:
        with st.spinner("Processing... This may take a few minutes"):
            try:
                # Create temporary directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Initialize components
                    downloader = YouTubeDownloader(output_dir=f"{temp_dir}/audio")
                    separator = StemSeparator(output_dir=f"{temp_dir}/stems")
                    arranger = SATBArranger()
                    midi_gen = MIDIGenerator(output_dir=f"{temp_dir}/midi")
                    
                    # Progress tracking
                    progress = st.progress(0)
                    status = st.empty()
                    
                    # Step 1: Get video info
                    status.text("Getting video information...")
                    video_info = downloader.get_video_info(youtube_url)
                    if video_info:
                        st.info(f"📹 **{video_info['title']}** by {video_info['uploader']}")
                    progress.progress(10)
                    
                    # Step 2: Download audio
                    status.text("Downloading audio...")
                    audio_path = downloader.download_audio(youtube_url)
                    progress.progress(30)
                    
                    # Step 3: Separate stems
                    status.text(f"Separating audio into {num_stems} stems...")
                    stem_paths = separator.separate_vocals(audio_path, stems=num_stems)
                    vocal_path = stem_paths.get('vocals', None)
                    
                    if not vocal_path:
                        raise ValueError("No vocal stem found")
                    progress.progress(60)
                    
                    # Step 4: Analyze melody
                    status.text("Analyzing vocal melody...")
                    melody_data = separator.extract_vocal_melody(vocal_path)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tempo", f"{melody_data['tempo']:.0f} BPM")
                    with col2:
                        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
                        st.metric("Key", keys[melody_data['key']])
                    with col3:
                        st.metric("Duration", f"{melody_data['duration']:.1f}s")
                    progress.progress(70)
                    
                    # Step 5: Create arrangement
                    status.text(f"Creating {arrangement_style} arrangement...")
                    parts = arranger.create_arrangement(melody_data, arrangement_style=arrangement_style)
                    progress.progress(85)
                    
                    # Step 6: Generate MIDI files
                    status.text("Generating MIDI files...")
                    midi_gen.set_midi_instruments(parts)
                    
                    # Export individual parts
                    midi_paths = midi_gen.export_parts(parts, filename_prefix="arrangement")
                    
                    # Export combined MIDI
                    combined_path = midi_gen.export_combined(parts, filename="satb_combined.mid")
                    
                    # Try to export score
                    score_path = midi_gen.export_score_pdf(parts, filename="satb_score.pdf")
                    
                    progress.progress(100)
                    status.text("Complete!")
                    
                    # Display results
                    st.success("✅ Arrangement created successfully!")
                    
                    st.header("Download Files")
                    
                    # Individual parts
                    st.subheader("Individual Voice Parts")
                    cols = st.columns(4)
                    for i, (voice, path) in enumerate(midi_paths.items()):
                        with cols[i]:
                            st.markdown(get_download_link(path, f"🎵 {voice.capitalize()}.mid"), 
                                      unsafe_allow_html=True)
                            
                    # Combined file
                    st.subheader("Combined Arrangement")
                    st.markdown(get_download_link(combined_path, "🎼 Complete SATB.mid"), 
                              unsafe_allow_html=True)
                    
                    # Score if available
                    if score_path and os.path.exists(score_path):
                        st.subheader("Score")
                        if score_path.endswith('.pdf'):
                            st.markdown(get_download_link(score_path, "📄 Score PDF"), 
                                      unsafe_allow_html=True)
                        else:
                            st.markdown(get_download_link(score_path, "📄 Score (MusicXML)"), 
                                      unsafe_allow_html=True)
                            
                    # Audio files if keeping
                    if keep_audio:
                        st.subheader("Audio Files")
                        st.markdown(get_download_link(audio_path, "🎧 Original Audio"), 
                                  unsafe_allow_html=True)
                        if vocal_path:
                            st.markdown(get_download_link(vocal_path, "🎤 Vocal Stem"), 
                                      unsafe_allow_html=True)
                            
                    # Instructions
                    with st.expander("📖 How to use these files"):
                        st.markdown("""
                        **MIDI Files:**
                        - Import into any DAW (Digital Audio Workstation)
                        - Open in notation software (MuseScore, Finale, Sibelius)
                        - Use with virtual instruments or synthesizers
                        
                        **Voice Ranges:**
                        - Soprano: C4 to A5
                        - Alto: G3 to D5
                        - Tenor: C3 to A4
                        - Bass: E2 to C4
                        
                        **Tips:**
                        - Adjust tempo and key as needed
                        - Fine-tune the harmonies to your preference
                        - Consider the vocal ranges of your choir
                        """)
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please check that the YouTube URL is valid and try again.")
                
    # Footer
    st.markdown("---")
    st.markdown(
        "Made with ❤️ using Spleeter, music21, and yt-dlp | "
        "[View on GitHub](https://github.com/yourusername/satb-arranger)"
    )


if __name__ == "__main__":
    main()