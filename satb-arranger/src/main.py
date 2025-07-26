"""Main CLI entry point for SATB Arranger tool."""

import argparse
import logging
from pathlib import Path

from youtube_downloader import YouTubeDownloader
from stem_separator import StemSeparator
from arranger import SATBArranger
from midi_generator import MIDIGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Create SATB arrangements from YouTube videos')
    parser.add_argument('--youtube-url', '-u', required=True, help='YouTube video URL')
    parser.add_argument('--output-dir', '-o', default='output', help='Output directory')
    parser.add_argument('--style', '-s', default='hymn', 
                       choices=['hymn', 'jazz', 'classical'],
                       help='Arrangement style')
    parser.add_argument('--stems', type=int, default=2, choices=[2, 4, 5],
                       help='Number of stems for separation')
    parser.add_argument('--keep-stems', action='store_true',
                       help='Keep separated audio stems')
    
    args = parser.parse_args()
    
    try:
        # Initialize components
        logger.info("Initializing SATB Arranger...")
        downloader = YouTubeDownloader(output_dir=f"{args.output_dir}/audio")
        separator = StemSeparator(output_dir=f"{args.output_dir}/stems")
        arranger = SATBArranger()
        midi_gen = MIDIGenerator(output_dir=f"{args.output_dir}/midi")
        
        # Step 1: Download audio from YouTube
        logger.info(f"Downloading audio from: {args.youtube_url}")
        video_info = downloader.get_video_info(args.youtube_url)
        if video_info:
            logger.info(f"Video: {video_info['title']} by {video_info['uploader']}")
            
        audio_path = downloader.download_audio(args.youtube_url)
        logger.info(f"Audio downloaded: {audio_path}")
        
        # Step 2: Separate stems
        logger.info(f"Separating audio into {args.stems} stems...")
        stem_paths = separator.separate_vocals(audio_path, stems=args.stems)
        
        # Get vocal stem path
        vocal_path = stem_paths.get('vocals', None)
        if not vocal_path:
            raise ValueError("No vocal stem found in separated audio")
            
        logger.info(f"Vocal stem extracted: {vocal_path}")
        
        # Step 3: Extract melodic information
        logger.info("Analyzing vocal melody...")
        melody_data = separator.extract_vocal_melody(vocal_path)
        logger.info(f"Detected tempo: {melody_data['tempo']} BPM")
        logger.info(f"Detected key: {melody_data['key']}")
        
        # Step 4: Create SATB arrangement
        logger.info(f"Creating {args.style} arrangement...")
        parts = arranger.create_arrangement(melody_data, arrangement_style=args.style)
        
        # Step 5: Generate MIDI files
        logger.info("Generating MIDI files...")
        
        # Set MIDI instruments
        midi_gen.set_midi_instruments(parts)
        
        # Export individual parts
        midi_paths = midi_gen.export_parts(parts, filename_prefix=Path(audio_path).stem)
        
        # Export combined MIDI
        combined_path = midi_gen.export_combined(parts, 
                                               filename=f"{Path(audio_path).stem}_satb.mid")
        
        # Try to export score
        score_path = midi_gen.export_score_pdf(parts, 
                                             filename=f"{Path(audio_path).stem}_score.pdf")
        
        # Clean up stems if not keeping
        if not args.keep_stems:
            logger.info("Cleaning up temporary files...")
            import shutil
            shutil.rmtree(f"{args.output_dir}/stems")
            
        # Summary
        logger.info("\n" + "="*50)
        logger.info("SATB Arrangement Complete!")
        logger.info("="*50)
        logger.info(f"Individual parts:")
        for voice, path in midi_paths.items():
            logger.info(f"  - {voice.capitalize()}: {path}")
        logger.info(f"Combined MIDI: {combined_path}")
        if score_path:
            logger.info(f"Score: {score_path}")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()