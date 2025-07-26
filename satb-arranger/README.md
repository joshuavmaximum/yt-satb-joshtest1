# SATB Arranger Tool

A comprehensive tool for choir arrangers that creates four-part SATB (Soprano, Alto, Tenor, Bass) arrangements from YouTube videos. The tool uses Spleeter for audio extraction and stem separation, then generates MIDI files for each vocal part.

## Features

- Download audio from YouTube videos
- Extract and separate vocal stems using Spleeter
- Analyze harmonic content and create four-part arrangements
- Generate individual MIDI files for each voice part (S, A, T, B)
- Web-based interface using Streamlit
- Audio playback and visualization

## Installation

1. Clone this repository
2. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install -y ffmpeg
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download Spleeter models (this will happen automatically on first use)

## Usage

### Web Interface (Recommended)
```bash
streamlit run src/app.py
```

### Command Line Interface
```bash
python src/main.py --youtube-url "YOUR_YOUTUBE_URL" --output-dir ./output
```

## Project Structure

```
satb-arranger/
├── src/
│   ├── main.py           # CLI entry point
│   ├── app.py            # Streamlit web interface
│   ├── youtube_downloader.py
│   ├── audio_processor.py
│   ├── stem_separator.py
│   ├── arranger.py
│   └── midi_generator.py
├── output/
│   ├── audio/           # Downloaded audio files
│   ├── stems/           # Separated audio stems
│   └── midi/            # Generated MIDI files
├── models/              # Spleeter models (auto-downloaded)
├── requirements.txt
└── README.md
```

## How It Works

1. **YouTube Download**: Uses yt-dlp to download audio from YouTube
2. **Stem Separation**: Spleeter separates vocals from accompaniment
3. **Harmonic Analysis**: Analyzes the harmonic content and melody
4. **Voice Arrangement**: Creates four-part harmony following voice-leading rules
5. **MIDI Generation**: Exports each voice part as a separate MIDI file

## Output

The tool generates:
- Individual MIDI files for each voice part (soprano.mid, alto.mid, tenor.mid, bass.mid)
- Combined MIDI file with all parts (satb_arrangement.mid)
- Separated audio stems for reference
- PDF score (optional, requires additional setup)

## Requirements

- Python 3.8+
- FFmpeg
- 4GB+ RAM recommended
- Internet connection for YouTube downloads