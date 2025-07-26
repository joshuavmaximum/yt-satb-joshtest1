"""SATB Arranger module for creating four-part vocal arrangements."""

import numpy as np
from music21 import stream, note, tempo, meter, key, chord, interval
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SATBArranger:
    """Create four-part SATB arrangements from melodic input."""
    
    # Voice ranges (MIDI note numbers)
    VOICE_RANGES = {
        'soprano': {'min': 60, 'max': 81},    # C4 to A5
        'alto': {'min': 55, 'max': 74},       # G3 to D5
        'tenor': {'min': 48, 'max': 69},      # C3 to A4
        'bass': {'min': 40, 'max': 60}        # E2 to C4
    }
    
    # Common chord progressions for harmonization
    PROGRESSIONS = {
        'major': {
            'I': ['I', 'iii', 'vi'],
            'ii': ['V', 'vii°'],
            'iii': ['vi', 'IV'],
            'IV': ['I', 'V', 'ii'],
            'V': ['I', 'vi'],
            'vi': ['ii', 'IV'],
            'vii°': ['I', 'iii']
        },
        'minor': {
            'i': ['i', 'III', 'VI'],
            'ii°': ['V', 'vii°'],
            'III': ['VI', 'iv'],
            'iv': ['i', 'V', 'ii°'],
            'V': ['i', 'VI'],
            'VI': ['ii°', 'iv'],
            'vii°': ['i', 'III']
        }
    }
    
    def __init__(self):
        self.parts = {
            'soprano': stream.Part(),
            'alto': stream.Part(),
            'tenor': stream.Part(),
            'bass': stream.Part()
        }
        
    def create_arrangement(self, melody_data, arrangement_style='hymn'):
        """
        Create a four-part SATB arrangement from melody data.
        
        Args:
            melody_data (dict): Melody information from stem separator
            arrangement_style (str): Style of arrangement ('hymn', 'jazz', 'classical')
            
        Returns:
            dict: Dictionary of music21 Part objects for each voice
        """
        # Extract melody information
        midi_notes = melody_data.get('midi_notes', [])
        tempo_bpm = melody_data.get('tempo', 120)
        key_num = melody_data.get('key', 0)
        
        # Filter out silence (0 values)
        melody_notes = [n for n in midi_notes if n > 0]
        
        if not melody_notes:
            raise ValueError("No valid melody notes found")
            
        # Determine key
        tonic = self._determine_key(melody_notes, key_num)
        
        # Set tempo and meter for all parts
        for part_name, part in self.parts.items():
            part.append(tempo.MetronomeMark(number=tempo_bpm))
            part.append(meter.TimeSignature('4/4'))
            part.append(key.Key(tonic))
            
        # Create arrangement based on style
        if arrangement_style == 'hymn':
            self._create_hymn_arrangement(melody_notes, tonic)
        elif arrangement_style == 'jazz':
            self._create_jazz_arrangement(melody_notes, tonic)
        else:  # classical
            self._create_classical_arrangement(melody_notes, tonic)
            
        return self.parts
        
    def _determine_key(self, melody_notes, key_num):
        """Determine the key of the piece."""
        # Map chromatic scale to key names
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Analyze melody to determine major/minor
        note_counts = {}
        for n in melody_notes:
            pitch_class = n % 12
            note_counts[pitch_class] = note_counts.get(pitch_class, 0) + 1
            
        # Simple heuristic: check for minor third
        tonic_pc = key_num % 12
        minor_third_pc = (tonic_pc + 3) % 12
        major_third_pc = (tonic_pc + 4) % 12
        
        is_minor = note_counts.get(minor_third_pc, 0) > note_counts.get(major_third_pc, 0)
        
        key_name = keys[tonic_pc]
        if is_minor:
            key_name = key_name.lower()
            
        return key_name
        
    def _create_hymn_arrangement(self, melody_notes, tonic):
        """Create a traditional hymn-style arrangement."""
        # Assign melody to soprano
        for midi_note in melody_notes:
            # Ensure note is in soprano range
            if midi_note < self.VOICE_RANGES['soprano']['min']:
                midi_note += 12
            elif midi_note > self.VOICE_RANGES['soprano']['max']:
                midi_note -= 12
                
            n = note.Note(midi_note)
            n.quarterLength = 1  # Default to quarter notes
            self.parts['soprano'].append(n)
            
        # Harmonize with basic triads
        current_key = key.Key(tonic)
        scale_degrees = [1, 4, 5, 1]  # I-IV-V-I progression
        
        for i, melody_note in enumerate(melody_notes):
            # Determine current chord
            scale_degree = scale_degrees[i % len(scale_degrees)]
            current_chord = self._get_chord_tones(current_key, scale_degree)
            
            # Alto: third of chord
            alto_note = self._find_closest_chord_tone(
                melody_note - 4, current_chord, self.VOICE_RANGES['alto']
            )
            
            # Tenor: fifth of chord
            tenor_note = self._find_closest_chord_tone(
                melody_note - 8, current_chord, self.VOICE_RANGES['tenor']
            )
            
            # Bass: root of chord
            bass_note = current_chord[0]
            while bass_note > self.VOICE_RANGES['bass']['max']:
                bass_note -= 12
            while bass_note < self.VOICE_RANGES['bass']['min']:
                bass_note += 12
                
            # Add notes to parts
            self.parts['alto'].append(note.Note(alto_note, quarterLength=1))
            self.parts['tenor'].append(note.Note(tenor_note, quarterLength=1))
            self.parts['bass'].append(note.Note(bass_note, quarterLength=1))
            
    def _create_jazz_arrangement(self, melody_notes, tonic):
        """Create a jazz-style arrangement with extended harmonies."""
        # Similar to hymn but with 7th chords and more complex progressions
        self._create_hymn_arrangement(melody_notes, tonic)  # Placeholder
        
    def _create_classical_arrangement(self, melody_notes, tonic):
        """Create a classical-style arrangement with counterpoint."""
        # Similar to hymn but with more independent voice leading
        self._create_hymn_arrangement(melody_notes, tonic)  # Placeholder
        
    def _get_chord_tones(self, key_obj, scale_degree):
        """Get chord tones for a given scale degree."""
        # Get the chord for this scale degree
        roman = key_obj.romanNumeral(scale_degree)
        chord_obj = roman.chord
        
        # Return MIDI note numbers
        return [p.midi for p in chord_obj.pitches]
        
    def _find_closest_chord_tone(self, target_note, chord_tones, voice_range):
        """Find the closest chord tone within voice range."""
        best_note = chord_tones[0]
        min_distance = float('inf')
        
        for tone in chord_tones:
            # Try different octaves
            for octave_shift in [-12, 0, 12]:
                candidate = tone + octave_shift
                
                # Check if in range
                if voice_range['min'] <= candidate <= voice_range['max']:
                    distance = abs(candidate - target_note)
                    if distance < min_distance:
                        min_distance = distance
                        best_note = candidate
                        
        return best_note
        
    def apply_voice_leading_rules(self):
        """Apply traditional voice leading rules to smooth the arrangement."""
        # Avoid parallel fifths and octaves
        # Minimize voice movement
        # Resolve leading tones
        # This is a placeholder for more sophisticated voice leading
        pass