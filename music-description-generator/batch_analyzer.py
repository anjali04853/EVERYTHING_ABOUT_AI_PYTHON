"""
Batch Music Analysis System
Process multiple audio files and generate comprehensive reports
"""

from pathlib import Path
import json
from music_analyzer import MusicAnalyzer, DescriptionGenerator
import pandas as pd
from datetime import datetime
from tqdm import tqdm


class BatchAnalyzer:
    """Process multiple audio files in batch"""
    
    def __init__(self):
        self.analyzer = MusicAnalyzer()
        self.generator = DescriptionGenerator()
        
    def analyze_directory(self, input_dir: str, output_dir: str = "batch_results"):
        """
        Analyze all audio files in a directory
        
        Args:
            input_dir: Directory containing audio files
            output_dir: Directory to save results
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Supported audio formats
        audio_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac']
        
        # Find all audio files
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(input_path.glob(f"*{ext}"))
            audio_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not audio_files:
            print(f"No audio files found in {input_dir}")
            return
        
        print(f"\nFound {len(audio_files)} audio files")
        print("="*60)
        
        # Process all files
        all_results = []
        
        for audio_file in tqdm(audio_files, desc="Analyzing tracks"):
            try:
                # Analyze
                results = self.analyzer.analyze_audio(str(audio_file))
                all_results.append(results)
                
                # Generate descriptions
                self._save_track_descriptions(results, output_path)
                
            except Exception as e:
                print(f"\nError analyzing {audio_file.name}: {e}")
                continue
        
        # Generate reports
        self._generate_summary_report(all_results, output_path)
        self._generate_csv_export(all_results, output_path)
        self._generate_genre_report(all_results, output_path)
        
        print(f"\n✓ Batch analysis complete! Results saved to {output_dir}/")
        
    def _save_track_descriptions(self, results: dict, output_path: Path):
        """Save individual track descriptions"""
        track_dir = output_path / "individual_tracks"
        track_dir.mkdir(exist_ok=True)
        
        # Save JSON
        json_file = track_dir / f"{Path(results['file_name']).stem}_analysis.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save descriptions
        descriptions = {
            'youtube': self.generator.generate_youtube_description(results),
            'podcast': self.generator.generate_podcast_description(results),
            'library': self.generator.generate_library_tags(results),
            'social': self.generator.generate_social_media(results)
        }
        
        for format_type, description in descriptions.items():
            desc_file = track_dir / f"{Path(results['file_name']).stem}_{format_type}.txt"
            with open(desc_file, 'w') as f:
                f.write(description)
    
    def _generate_summary_report(self, results: list, output_path: Path):
        """Generate comprehensive summary report"""
        report = []
        report.append("="*70)
        report.append("MUSIC LIBRARY ANALYSIS REPORT")
        report.append("="*70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Tracks Analyzed: {len(results)}")
        report.append("")
        
        # Genre distribution
        genres = {}
        for r in results:
            genre = r['genre']
            genres[genre] = genres.get(genre, 0) + 1
        
        report.append("GENRE DISTRIBUTION")
        report.append("-"*70)
        for genre, count in sorted(genres.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(results)) * 100
            report.append(f"  {genre}: {count} tracks ({percentage:.1f}%)")
        report.append("")
        
        # Mood distribution
        moods = {}
        for r in results:
            mood = r['mood']
            moods[mood] = moods.get(mood, 0) + 1
        
        report.append("MOOD DISTRIBUTION")
        report.append("-"*70)
        for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(results)) * 100
            report.append(f"  {mood}: {count} tracks ({percentage:.1f}%)")
        report.append("")
        
        # Tempo analysis
        tempos = [r['tempo'] for r in results]
        report.append("TEMPO ANALYSIS")
        report.append("-"*70)
        report.append(f"  Average Tempo: {sum(tempos)/len(tempos):.1f} BPM")
        report.append(f"  Fastest Track: {max(tempos):.1f} BPM")
        report.append(f"  Slowest Track: {min(tempos):.1f} BPM")
        report.append("")
        
        # Energy levels
        energies = [r['energy'] for r in results]
        report.append("ENERGY LEVELS")
        report.append("-"*70)
        report.append(f"  Average Energy: {sum(energies)/len(energies):.1f}%")
        high_energy = len([e for e in energies if e > 70])
        medium_energy = len([e for e in energies if 40 <= e <= 70])
        low_energy = len([e for e in energies if e < 40])
        report.append(f"  High Energy (>70%): {high_energy} tracks")
        report.append(f"  Medium Energy (40-70%): {medium_energy} tracks")
        report.append(f"  Low Energy (<40%): {low_energy} tracks")
        report.append("")
        
        # Key distribution
        keys = {}
        for r in results:
            key = r['key']
            keys[key] = keys.get(key, 0) + 1
        
        report.append("KEY DISTRIBUTION")
        report.append("-"*70)
        for key, count in sorted(keys.items(), key=lambda x: x[1], reverse=True)[:10]:
            report.append(f"  {key}: {count} tracks")
        report.append("")
        
        # Top tracks by feature
        report.append("TOP TRACKS")
        report.append("-"*70)
        
        # Most energetic
        most_energetic = sorted(results, key=lambda x: x['energy'], reverse=True)[:3]
        report.append("  Most Energetic:")
        for i, track in enumerate(most_energetic, 1):
            report.append(f"    {i}. {track['file_name']} ({track['energy']}%)")
        report.append("")
        
        # Most danceable
        most_danceable = sorted(results, key=lambda x: x['danceability'], reverse=True)[:3]
        report.append("  Most Danceable:")
        for i, track in enumerate(most_danceable, 1):
            report.append(f"    {i}. {track['file_name']} ({track['danceability']}%)")
        report.append("")
        
        # Most positive
        most_positive = sorted(results, key=lambda x: x['valence'], reverse=True)[:3]
        report.append("  Most Positive:")
        for i, track in enumerate(most_positive, 1):
            report.append(f"    {i}. {track['file_name']} ({track['valence']}%)")
        report.append("")
        
        report.append("="*70)
        
        # Save report
        report_file = output_path / "analysis_summary.txt"
        with open(report_file, 'w') as f:
            f.write('\n'.join(report))
        
        # Also print to console
        print("\n" + '\n'.join(report))
    
    def _generate_csv_export(self, results: list, output_path: Path):
        """Export results to CSV for easy analysis"""
        df = pd.DataFrame(results)
        
        # Flatten instruments list
        df['instruments'] = df['instruments'].apply(lambda x: ', '.join(x))
        
        # Save CSV
        csv_file = output_path / "music_analysis.csv"
        df.to_csv(csv_file, index=False)
        print(f"\n✓ Exported data to CSV: {csv_file}")
    
    def _generate_genre_report(self, results: list, output_path: Path):
        """Generate detailed genre-specific reports"""
        genre_dir = output_path / "genre_reports"
        genre_dir.mkdir(exist_ok=True)
        
        # Group by genre
        by_genre = {}
        for r in results:
            genre = r['genre']
            if genre not in by_genre:
                by_genre[genre] = []
            by_genre[genre].append(r)
        
        # Generate report for each genre
        for genre, tracks in by_genre.items():
            report = []
            report.append(f"{'='*60}")
            report.append(f"{genre.upper()} GENRE REPORT")
            report.append(f"{'='*60}")
            report.append(f"Total Tracks: {len(tracks)}")
            report.append("")
            
            # Sub-genres
            sub_genres = {}
            for t in tracks:
                sg = t['sub_genre']
                sub_genres[sg] = sub_genres.get(sg, 0) + 1
            
            report.append("Sub-Genres:")
            for sg, count in sorted(sub_genres.items(), key=lambda x: x[1], reverse=True):
                report.append(f"  • {sg}: {count} tracks")
            report.append("")
            
            # Average features
            avg_tempo = sum(t['tempo'] for t in tracks) / len(tracks)
            avg_energy = sum(t['energy'] for t in tracks) / len(tracks)
            avg_dance = sum(t['danceability'] for t in tracks) / len(tracks)
            
            report.append("Average Characteristics:")
            report.append(f"  • Tempo: {avg_tempo:.1f} BPM")
            report.append(f"  • Energy: {avg_energy:.1f}%")
            report.append(f"  • Danceability: {avg_dance:.1f}%")
            report.append("")
            
            # Track list
            report.append("Tracks:")
            for track in sorted(tracks, key=lambda x: x['file_name']):
                report.append(f"  • {track['file_name']}")
                report.append(f"    {track['tempo']} BPM | {track['key']} | {track['mood']}")
            
            report.append(f"{'='*60}")
            
            # Save genre report
            genre_file = genre_dir / f"{genre.lower().replace(' ', '_')}_report.txt"
            with open(genre_file, 'w') as f:
                f.write('\n'.join(report))


def main():
    """Main entry point for batch analysis"""
    import sys
    
    if len(sys.argv) < 2:
        print("Batch Music Analyzer")
        print("="*50)
        print("Usage: python batch_analyzer.py <directory>")
        print("\nExample:")
        print("  python batch_analyzer.py sample_tracks/")
        print("\nThis will analyze all audio files in the directory and")
        print("generate comprehensive reports and descriptions.")
        return
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "batch_results"
    
    batch = BatchAnalyzer()
    batch.analyze_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()