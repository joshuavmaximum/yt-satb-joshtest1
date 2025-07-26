#!/usr/bin/env python3
"""Example usage of the SATB Arranger tool."""

import sys
sys.path.append('src')

from youtube_downloader import YouTubeDownloader
from stem_separator import StemSeparator
from arranger import SATBArranger
from midi_generator import MIDIGenerator


def main():
    # Example YouTube URL (replace with actual URL)
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("SATB Arranger Example")
    print("=" * 50)
    
    # Initialize components
    downloader = YouTubeDownloader()
    separator = StemSeparator()
    arranger = SATBArranger()
    midi_gen = MIDIGenerator()
    
    try:
        # Step 1: Download audio
        print("\n1. Downloading audio from YouTube...")
        audio_path = downloader.download_audio(youtube_url)
        print(f"   ✓ Audio saved to: {audio_path}")
        
        # Step 2: Separate stems
        print("\n2. Separating vocals from accompaniment...")
        stems = separator.separate_vocals(audio_path, stems=2)
        vocal_path = stems['vocals']
        print(f"   ✓ Vocals extracted to: {vocal_path}")
        
        # Step 3: Analyze melody
        print("\n3. Analyzing vocal melody...")
        melody_data = separator.extract_vocal_melody(vocal_path)
        print(f"   ✓ Tempo: {melody_data['tempo']:.0f} BPM")
        print(f"   ✓ Key: {melody_data['key']}")
        
        # Step 4: Create arrangement
        print("\n4. Creating SATB arrangement...")
        parts = arranger.create_arrangement(melody_data, arrangement_style='hymn')
        print("   ✓ Four-part harmony created")
        
        # Step 5: Export MIDI
        print("\n5. Exporting MIDI files...")
        midi_gen.set_midi_instruments(parts)
        midi_paths = midi_gen.export_parts(parts)
        combined_path = midi_gen.export_combined(parts)
        
        print("\n✅ Success! Files created:")
        for voice, path in midi_paths.items():
            print(f"   - {voice}: {path}")
        print(f"   - Combined: {combined_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        

if __name__ == "__main__":
    main()