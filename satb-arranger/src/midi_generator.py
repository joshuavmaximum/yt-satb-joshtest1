"""MIDI generator module for exporting arrangements."""

from pathlib import Path
from music21 import stream, midi
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MIDIGenerator:
    """Generate MIDI files from music21 arrangements."""
    
    def __init__(self, output_dir="output/midi"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def export_parts(self, parts, filename_prefix="arrangement"):
        """
        Export individual MIDI files for each voice part.
        
        Args:
            parts (dict): Dictionary of music21 Part objects
            filename_prefix (str): Prefix for output filenames
            
        Returns:
            dict: Paths to generated MIDI files
        """
        midi_paths = {}
        
        for voice_name, part in parts.items():
            # Set part name
            part.partName = voice_name.capitalize()
            
            # Create individual MIDI file
            midi_filename = f"{filename_prefix}_{voice_name}.mid"
            midi_path = self.output_dir / midi_filename
            
            try:
                # Export to MIDI
                part.write('midi', fp=str(midi_path))
                midi_paths[voice_name] = str(midi_path)
                logger.info(f"Exported {voice_name} to {midi_path}")
                
            except Exception as e:
                logger.error(f"Error exporting {voice_name}: {str(e)}")
                raise
                
        return midi_paths
        
    def export_combined(self, parts, filename="satb_arrangement.mid"):
        """
        Export all parts combined into a single MIDI file.
        
        Args:
            parts (dict): Dictionary of music21 Part objects
            filename (str): Output filename
            
        Returns:
            str: Path to generated MIDI file
        """
        # Create a score with all parts
        score = stream.Score()
        
        # Add parts in SATB order
        for voice in ['soprano', 'alto', 'tenor', 'bass']:
            if voice in parts:
                parts[voice].partName = voice.capitalize()
                score.append(parts[voice])
                
        # Export combined MIDI
        midi_path = self.output_dir / filename
        
        try:
            score.write('midi', fp=str(midi_path))
            logger.info(f"Exported combined arrangement to {midi_path}")
            return str(midi_path)
            
        except Exception as e:
            logger.error(f"Error exporting combined MIDI: {str(e)}")
            raise
            
    def export_score_pdf(self, parts, filename="satb_arrangement.pdf"):
        """
        Export arrangement as PDF score (requires MuseScore or Lilypond).
        
        Args:
            parts (dict): Dictionary of music21 Part objects
            filename (str): Output filename
            
        Returns:
            str: Path to generated PDF file (if successful)
        """
        # Create a score with all parts
        score = stream.Score()
        
        # Add parts in SATB order
        for voice in ['soprano', 'alto', 'tenor', 'bass']:
            if voice in parts:
                parts[voice].partName = voice.capitalize()
                score.append(parts[voice])
                
        # Try to export as PDF
        pdf_path = self.output_dir / filename
        
        try:
            # This requires MuseScore or Lilypond to be installed
            score.write('lily.pdf', fp=str(pdf_path))
            logger.info(f"Exported score to {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            logger.warning(f"Could not export PDF (install MuseScore/Lilypond): {str(e)}")
            # Try MusicXML as alternative
            try:
                xml_path = self.output_dir / filename.replace('.pdf', '.xml')
                score.write('musicxml', fp=str(xml_path))
                logger.info(f"Exported MusicXML to {xml_path}")
                return str(xml_path)
            except Exception as e2:
                logger.error(f"Error exporting score: {str(e2)}")
                return None
                
    def set_midi_instruments(self, parts, instruments=None):
        """
        Set MIDI instruments for each part.
        
        Args:
            parts (dict): Dictionary of music21 Part objects
            instruments (dict): Optional mapping of voice names to MIDI program numbers
        """
        if instruments is None:
            # Default to choir voices
            instruments = {
                'soprano': 52,  # Choir Aahs
                'alto': 52,     # Choir Aahs
                'tenor': 52,    # Choir Aahs
                'bass': 52      # Choir Aahs
            }
            
        for voice_name, part in parts.items():
            if voice_name in instruments:
                # Set MIDI program for this part
                part.append(midi.MidiProgram(instruments[voice_name]))