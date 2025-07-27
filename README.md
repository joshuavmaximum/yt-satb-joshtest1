# YouTube Audio to MIDI Converter

A modern web application that extracts audio from YouTube videos and converts it into 5 separate MIDI files using the Spleeter API for audio separation.

## Features

- **YouTube URL Validation**: Validates YouTube URLs before processing
- **Audio Extraction**: Downloads audio from YouTube videos using yt-dlp
- **Audio Separation**: Uses Spleeter API to separate audio into 5 stems:
  - Vocals
  - Drums
  - Bass
  - Piano
  - Other instruments
- **MIDI Conversion**: Converts each audio stem to MIDI format
- **Download Support**: Download individual MIDI files for each track
- **Progress Tracking**: Real-time progress updates during processing
- **Responsive Design**: Works on desktop and mobile devices

## How It Works

1. **Extract Audio**: Downloads and extracts audio from the YouTube video
2. **Split Audio**: Uses Spleeter to separate the audio into 5 stems
3. **Convert to MIDI**: Converts each audio stem to MIDI using pitch detection
4. **Download Files**: Provides individual MIDI files for each instrument track

## Usage

1. Open `index.html` in your web browser
2. Enter a valid YouTube URL in the input field
3. Click "Validate" to verify the URL
4. Select your preferred audio quality and MIDI resolution
5. Click "Process Video" to start the conversion
6. Wait for the processing to complete
7. Download the generated MIDI files

## Processing Options

### Audio Quality
- **High Quality**: Best audio quality, larger file size
- **Medium Quality**: Balanced quality and file size (recommended)
- **Low Quality**: Smaller file size, lower quality

### MIDI Resolution
- **480 Ticks/Beat**: High precision MIDI timing
- **240 Ticks/Beat**: Standard MIDI timing (recommended)
- **120 Ticks/Beat**: Lower precision, smaller file size

## File Structure

```
youtube-midi-converter/
├── index.html          # Main application file
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
└── README.md          # This file
```

## Technical Details

### Audio Processing Pipeline

1. **YouTube Download**: Uses yt-dlp to download audio from YouTube
2. **Spleeter Separation**: Separates audio into 5 stems using Spleeter
3. **MIDI Conversion**: Converts audio to MIDI using pitch detection algorithms
4. **File Generation**: Creates individual MIDI files for each track

### Supported YouTube URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

### MIDI File Format

Each generated MIDI file contains:
- Track information (instrument type)
- Note events (pitch, velocity, duration)
- Timing information (tempo, time signatures)
- Controller data (volume, pan, effects)

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## API Integration

The application includes a `SpleeterAPI` class for integrating with Spleeter services:

```javascript
const spleeter = new SpleeterAPI();
spleeter.setApiKey('your-api-key');

// Separate audio into stems
const separatedTracks = await spleeter.separateAudio(audioData, 5);

// Convert to MIDI
const midiFile = await spleeter.convertToMIDI(audioTrack, {
    resolution: 240,
    quality: 'medium'
});
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid YouTube URLs
- Network connectivity issues
- Audio processing failures
- MIDI conversion errors
- File download problems

## Performance Considerations

- Processing time depends on video length and audio quality
- Large videos may take several minutes to process
- Progress is shown in real-time during processing
- Results are cached for faster subsequent downloads

## Security

- All processing is done client-side where possible
- No audio data is stored on servers
- API keys are handled securely
- Downloads are generated locally

## Future Enhancements

- Support for more audio formats
- Additional MIDI export options
- Real-time audio preview
- Batch processing capabilities
- Integration with music production software

## Troubleshooting

### Common Issues

1. **URL Validation Fails**
   - Ensure the YouTube URL is correct
   - Check that the video is publicly accessible
   - Try copying the URL directly from YouTube

2. **Processing Takes Too Long**
   - Reduce audio quality setting
   - Try shorter videos first
   - Check internet connection

3. **Download Fails**
   - Check browser download settings
   - Ensure sufficient disk space
   - Try a different browser

### Getting Help

If you encounter issues:
1. Check the browser console for error messages
2. Verify your internet connection
3. Try refreshing the page
4. Contact support with specific error details

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Spleeter team for audio separation technology
- YouTube for video hosting
- Web Audio API for browser audio processing
- Font Awesome for icons