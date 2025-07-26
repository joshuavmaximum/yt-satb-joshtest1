"""Stem separation module using Spleeter."""

import os
from pathlib import Path
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
import logging
import numpy as np
import soundfile as sf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StemSeparator:
    def __init__(self, output_dir="output/stems", model_dir="models"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Set Spleeter model directory
        os.environ['MODEL_PATH'] = str(self.model_dir)
        
        # Initialize separators for different configurations
        self.separator_2stems = None
        self.separator_4stems = None
        self.separator_5stems = None
        self.audio_adapter = AudioAdapter.default()
        
    def separate_vocals(self, audio_path, stems=2):
        """
        Separate vocals from audio file.
        
        Args:
            audio_path (str): Path to input audio file
            stems (int): Number of stems (2, 4, or 5)
            
        Returns:
            dict: Paths to separated audio files
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Initialize appropriate separator
        if stems == 2:
            if not self.separator_2stems:
                logger.info("Initializing 2-stem separator (vocals/accompaniment)")
                self.separator_2stems = Separator('spleeter:2stems')
            separator = self.separator_2stems
        elif stems == 4:
            if not self.separator_4stems:
                logger.info("Initializing 4-stem separator (vocals/drums/bass/other)")
                self.separator_4stems = Separator('spleeter:4stems')
            separator = self.separator_4stems
        elif stems == 5:
            if not self.separator_5stems:
                logger.info("Initializing 5-stem separator (vocals/drums/bass/piano/other)")
                self.separator_5stems = Separator('spleeter:5stems')
            separator = self.separator_5stems
        else:
            raise ValueError(f"Invalid number of stems: {stems}. Must be 2, 4, or 5.")
            
        # Create output directory for this file
        file_stem = audio_path.stem
        output_path = self.output_dir / file_stem
        output_path.mkdir(exist_ok=True)
        
        try:
            logger.info(f"Separating {audio_path} into {stems} stems...")
            
            # Load audio
            waveform, sample_rate = self.audio_adapter.load(str(audio_path))
            
            # Perform separation
            prediction = separator.separate(waveform)
            
            # Save separated stems
            stem_paths = {}
            for stem_name, audio_data in prediction.items():
                stem_file = output_path / f"{stem_name}.wav"
                
                # Ensure audio data is in the correct shape
                if len(audio_data.shape) == 1:
                    audio_data = audio_data.reshape(-1, 1)
                
                # Save the stem
                sf.write(str(stem_file), audio_data, sample_rate)
                stem_paths[stem_name] = str(stem_file)
                logger.info(f"Saved {stem_name} to {stem_file}")
                
            return stem_paths
            
        except Exception as e:
            logger.error(f"Error during stem separation: {str(e)}")
            raise
            
    def extract_vocal_melody(self, vocal_path):
        """
        Extract melodic information from vocal stem.
        
        Args:
            vocal_path (str): Path to vocal audio file
            
        Returns:
            dict: Extracted melodic features
        """
        import librosa
        
        try:
            # Load vocal audio
            y, sr = librosa.load(vocal_path, sr=None)
            
            # Extract pitch using piptrack
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            
            # Extract fundamental frequency (f0)
            f0 = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    f0.append(pitch)
                else:
                    f0.append(0)
                    
            # Convert to MIDI notes
            midi_notes = []
            for freq in f0:
                if freq > 0:
                    midi_note = librosa.hz_to_midi(freq)
                    midi_notes.append(int(round(midi_note)))
                else:
                    midi_notes.append(0)
                    
            # Extract tempo
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Extract key
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            key = np.argmax(np.mean(chroma, axis=1))
            
            return {
                'frequencies': f0,
                'midi_notes': midi_notes,
                'tempo': float(tempo),
                'key': int(key),
                'sample_rate': sr,
                'duration': len(y) / sr
            }
            
        except Exception as e:
            logger.error(f"Error extracting vocal melody: {str(e)}")
            raise