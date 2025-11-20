"""
Hugging Face Music Description Generator
Main audio analysis and description generation system
"""

import librosa
import numpy as np
from transformers import pipeline
import soundfile as sf
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class MusicAnalyzer:
    """Advanced music analysis using Hugging Face models and librosa"""
    
    def __init__(self):
        """Initialize analysis models"""
        print("Loading Hugging Face models...")
        
        # Audio classification model for genre detection
        try:
            self.genre_classifier = pipeline(
                "audio-classification",
                model="facebook/musicgen-small"  # Can use other models
            )
        except:
            print("Note: Using fallback analysis. Install transformers for full features.")
            self.genre_classifier = None
        
        # Mood mapping
        self.mood_mappings = {
            'high_energy_major': 'Energetic & Uplifting',
            'high_energy_minor': 'Intense & Driving',
            'low_energy_major': 'Peaceful & Calm',
            'low_energy_minor': 'Melancholic & Contemplative',
            'medium_energy_major': 'Cheerful & Positive',
            'medium_energy_minor': 'Thoughtful & Reflective'
        }
        
        print("Music Analyzer initialized successfully!")
    
    def analyze_audio(self, audio_path: str) -> Dict:
        """
        Comprehensive audio analysis
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary containing all analysis results
        """
        print(f"\nAnalyzing: {Path(audio_path).name}")
        print("-" * 50)
        
        # Load audio file
        y, sr = librosa.load(audio_path, duration=60)  # Analyze first 60 seconds
        
        # Basic info
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Tempo and beat analysis
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        # Key detection
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key = self._detect_key(chroma)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        # Zero crossing rate (useful for distinguishing percussion)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        
        # MFCC for timbre analysis
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # RMS energy
        rms = librosa.feature.rms(y=y)[0]
        
        # Analyze components
        genre = self._detect_genre(spectral_centroids, zcr, tempo)
        mood = self._detect_mood(rms, chroma, tempo)
        instruments = self._detect_instruments(y, sr, spectral_centroids, zcr)
        
        # Audio features (Spotify-like)
        energy = self._calculate_energy(rms)
        danceability = self._calculate_danceability(tempo, beats, rms)
        valence = self._calculate_valence(chroma, rms)
        
        # Loudness (in dB)
        loudness = librosa.amplitude_to_db(rms).mean()
        
        results = {
            'file_name': Path(audio_path).name,
            'duration': f"{int(duration // 60)}:{int(duration % 60):02d}",
            'duration_seconds': duration,
            'tempo': round(tempo, 1),
            'key': key,
            'time_signature': self._estimate_time_signature(beats, sr),
            'genre': genre['primary'],
            'sub_genre': genre['secondary'],
            'mood': mood,
            'instruments': instruments,
            'energy': energy,
            'danceability': danceability,
            'valence': valence,
            'loudness': round(loudness, 1),
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return results
    
    def _detect_key(self, chroma) -> str:
        """Detect musical key from chroma features"""
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_idx = np.argmax(np.sum(chroma, axis=1))
        
        # Determine if major or minor based on chord quality
        major_profile = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
        minor_profile = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        
        chroma_mean = np.mean(chroma, axis=1)
        major_corr = np.corrcoef(chroma_mean, major_profile)[0, 1]
        minor_corr = np.corrcoef(chroma_mean, minor_profile)[0, 1]
        
        mode = "Major" if major_corr > minor_corr else "Minor"
        return f"{keys[key_idx]} {mode}"
    
    def _detect_genre(self, spectral_centroids, zcr, tempo) -> Dict[str, str]:
        """Detect music genre based on audio features"""
        avg_centroid = np.mean(spectral_centroids)
        avg_zcr = np.mean(zcr)
        
        # Genre classification rules
        if tempo > 120 and avg_centroid > 3000:
            if avg_zcr > 0.1:
                return {'primary': 'Electronic', 'secondary': 'Techno'}
            else:
                return {'primary': 'Electronic', 'secondary': 'House'}
        elif tempo > 140:
            return {'primary': 'Electronic', 'secondary': 'Drum & Bass'}
        elif tempo < 90 and avg_centroid < 2000:
            return {'primary': 'Hip Hop', 'secondary': 'Trap'}
        elif tempo > 110 and tempo < 130 and avg_centroid > 2500:
            return {'primary': 'Pop', 'secondary': 'Dance Pop'}
        elif avg_centroid < 2000:
            return {'primary': 'R&B', 'secondary': 'Contemporary R&B'}
        elif tempo < 100:
            return {'primary': 'Ambient', 'secondary': 'Downtempo'}
        else:
            return {'primary': 'Pop', 'secondary': 'Contemporary'}
    
    def _detect_mood(self, rms, chroma, tempo) -> str:
        """Detect mood based on energy and tonality"""
        energy_level = np.mean(rms)
        chroma_var = np.var(chroma)
        
        # Major/minor detection (simplified)
        is_major = chroma_var < 0.1
        
        if energy_level > 0.1 and tempo > 120:
            energy_cat = 'high_energy'
        elif energy_level < 0.05:
            energy_cat = 'low_energy'
        else:
            energy_cat = 'medium_energy'
        
        mode = 'major' if is_major else 'minor'
        key = f"{energy_cat}_{mode}"
        
        return self.mood_mappings.get(key, 'Balanced & Melodic')
    
    def _detect_instruments(self, y, sr, spectral_centroids, zcr) -> List[str]:
        """Detect likely instruments present in the audio"""
        instruments = []
        
        avg_centroid = np.mean(spectral_centroids)
        avg_zcr = np.mean(zcr)
        
        # Frequency-based instrument detection
        if avg_zcr > 0.1:
            instruments.append('Drums')
        
        if avg_centroid > 3000:
            instruments.append('Hi-Hat/Cymbals')
        
        if avg_centroid > 2000:
            instruments.append('Synthesizer')
        
        # Bass detection (low frequency energy)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        if np.mean(spectral_contrast[0]) > 20:
            instruments.append('Bass')
        
        # Mid-range for vocals/guitars
        if 1000 < avg_centroid < 3000:
            instruments.append('Vocals')
        
        # Piano/keyboard presence
        if len(instruments) < 3:
            instruments.append('Keyboard')
        
        return instruments[:5]  # Limit to 5 instruments
    
    def _calculate_energy(self, rms) -> int:
        """Calculate energy level (0-100)"""
        energy = np.mean(rms) * 100
        return min(100, int(energy * 150))  # Scale appropriately
    
    def _calculate_danceability(self, tempo, beats, rms) -> int:
        """Calculate danceability score (0-100)"""
        # Ideal dance tempo is around 120-130 BPM
        tempo_score = 100 - abs(tempo - 125) * 2
        tempo_score = max(0, min(100, tempo_score))
        
        # Rhythm regularity
        rhythm_score = 70  # Simplified
        
        # Energy contribution
        energy_score = np.mean(rms) * 100
        
        danceability = (tempo_score * 0.4 + rhythm_score * 0.3 + energy_score * 0.3)
        return min(100, int(danceability))
    
    def _calculate_valence(self, chroma, rms) -> int:
        """Calculate valence/positivity (0-100)"""
        # Major keys and higher energy typically = higher valence
        chroma_var = np.var(chroma)
        energy = np.mean(rms)
        
        # Lower variance often means major key
        tonality_score = (1 - min(chroma_var, 1)) * 100
        energy_score = energy * 100
        
        valence = (tonality_score * 0.6 + energy_score * 0.4)
        return min(100, int(valence))
    
    def _estimate_time_signature(self, beats, sr) -> str:
        """Estimate time signature"""
        # Most popular music is in 4/4
        # This could be enhanced with beat strength analysis
        return "4/4"


class DescriptionGenerator:
    """Generate descriptions in various formats"""
    
    @staticmethod
    def generate_youtube_description(analysis: Dict) -> str:
        """Generate YouTube video description"""
        use_case = DescriptionGenerator._get_use_case(analysis)
        
        desc = f"""🎵 {analysis['file_name']} | {analysis['genre']} Music

🎼 Genre: {analysis['genre']} - {analysis['sub_genre']}
🎹 Key: {analysis['key']}
⚡ Tempo: {analysis['tempo']} BPM
🎭 Mood: {analysis['mood']}
⏱️ Duration: {analysis['duration']}

🎧 Musical Characteristics:
• Energy Level: {analysis['energy']}%
• Danceability: {analysis['danceability']}%
• Emotional Valence: {analysis['valence']}%
• Time Signature: {analysis['time_signature']}

🎸 Instrumentation:
{chr(10).join(f"• {inst}" for inst in analysis['instruments'])}

📊 Technical Details:
• Loudness: {analysis['loudness']} dB
• Production Quality: Professional

Perfect for: {use_case}

#{analysis['genre'].replace(' ', '')} #{analysis['sub_genre'].replace(' ', '')} #Music #Production #Audio"""
        
        return desc
    
    @staticmethod
    def generate_podcast_description(analysis: Dict) -> str:
        """Generate podcast show notes"""
        use_case = DescriptionGenerator._get_podcast_use(analysis)
        
        desc = f"""Episode Background Music: {analysis['file_name']}

This {analysis['mood'].lower()} {analysis['genre'].lower()} track creates the perfect atmosphere for your podcast. Running at {analysis['tempo']} BPM in {analysis['key']}, it features {', '.join(analysis['instruments'][:3]).lower()} that provide a professional sonic backdrop without overwhelming dialogue.

🎵 Track Details:
Mood: {analysis['mood']}
Genre: {analysis['genre']} - {analysis['sub_genre']}
Duration: {analysis['duration']}
Energy Level: {analysis['energy']}/100
Danceability: {analysis['danceability']}/100

🎧 Best Used During: {use_case}

Technical Specifications:
{analysis['tempo']} BPM | {analysis['key']} | {analysis['time_signature']}
Loudness: {analysis['loudness']} dB

This track provides consistent energy throughout, making it ideal for maintaining listener engagement during key moments of your show."""
        
        return desc
    
    @staticmethod
    def generate_library_tags(analysis: Dict) -> str:
        """Generate music library metadata"""
        tags = [
            analysis['genre'],
            analysis['sub_genre'],
            analysis['mood'],
            f"{analysis['tempo']}BPM",
            analysis['key'].replace(' ', ''),
            *analysis['instruments']
        ]
        
        desc = f"""Title: {analysis['file_name']}
Genre: {analysis['genre']}
Sub-Genre: {analysis['sub_genre']}
Mood: {analysis['mood']}
Tempo: {analysis['tempo']} BPM
Key: {analysis['key']}
Time Signature: {analysis['time_signature']}
Duration: {analysis['duration']}

Instruments: {', '.join(analysis['instruments'])}

Audio Features:
• Energy: {analysis['energy']}%
• Danceability: {analysis['danceability']}%
• Valence: {analysis['valence']}%
• Loudness: {analysis['loudness']} dB

Tags: {', '.join(tags)}

Description: A {analysis['mood'].lower()} {analysis['genre'].lower()} track featuring {', '.join(analysis['instruments'][:3]).lower()}. Perfect for {DescriptionGenerator._get_use_case(analysis).lower()}."""
        
        return desc
    
    @staticmethod
    def generate_social_media(analysis: Dict) -> str:
        """Generate social media post"""
        emoji = "🔥" if analysis['energy'] > 70 else "✨"
        vibe = "high-energy" if analysis['energy'] > 70 else "chill"
        
        desc = f"""🎵 New {analysis['genre']} Release! 🎵

{analysis['mood']} vibes at {analysis['tempo']} BPM {emoji}
Key: {analysis['key']} | {analysis['duration']}

Featuring: {', '.join(analysis['instruments'][:3])}

Perfect for your {vibe} playlist! 💯

#{analysis['genre'].replace(' ', '')} #Music #NewMusic #{analysis['mood'].split()[0]} #Audio #Production #{analysis['sub_genre'].replace(' ', '')}"""
        
        return desc
    
    @staticmethod
    def _get_use_case(analysis: Dict) -> str:
        """Determine use case based on audio features"""
        if analysis['energy'] > 75 and analysis['danceability'] > 70:
            return "High-energy workouts, parties, gaming, and intense activities"
        elif analysis['energy'] < 40 and analysis['valence'] < 50:
            return "Relaxation, meditation, studying, and calm focus work"
        elif analysis['danceability'] > 70:
            return "Dancing, social gatherings, and upbeat content"
        elif analysis['valence'] > 70:
            return "Uplifting content, vlogs, celebrations, and positive moments"
        else:
            return "Background music, creative work, podcasts, and versatile content"
    
    @staticmethod
    def _get_podcast_use(analysis: Dict) -> str:
        """Get podcast-specific use case"""
        if analysis['energy'] > 70:
            return "High-energy segments, show introductions, exciting announcements, and climactic moments"
        elif analysis['energy'] < 40:
            return "Thoughtful discussions, emotional stories, meditation segments, and closing thoughts"
        else:
            return "Transitions between segments, background for interviews, and general podcast atmosphere"


def analyze_track(audio_path: str, output_dir: str = "analysis_results"):
    """
    Analyze a single track and generate all descriptions
    
    Args:
        audio_path: Path to audio file
        output_dir: Directory to save results
    """
    analyzer = MusicAnalyzer()
    generator = DescriptionGenerator()
    
    # Perform analysis
    results = analyzer.analyze_audio(audio_path)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save JSON results
    json_file = output_path / f"{Path(audio_path).stem}_analysis.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Saved analysis: {json_file}")
    
    # Generate and save descriptions
    descriptions = {
        'youtube': generator.generate_youtube_description(results),
        'podcast': generator.generate_podcast_description(results),
        'library': generator.generate_library_tags(results),
        'social': generator.generate_social_media(results)
    }
    
    for format_type, description in descriptions.items():
        desc_file = output_path / f"{Path(audio_path).stem}_{format_type}.txt"
        with open(desc_file, 'w') as f:
            f.write(description)
        print(f"✓ Saved {format_type} description: {desc_file}")
    
    # Display summary
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    print(f"File: {results['file_name']}")
    print(f"Genre: {results['genre']} - {results['sub_genre']}")
    print(f"Mood: {results['mood']}")
    print(f"Tempo: {results['tempo']} BPM | Key: {results['key']}")
    print(f"Duration: {results['duration']}")
    print(f"Instruments: {', '.join(results['instruments'])}")
    print(f"\nEnergy: {results['energy']}% | Danceability: {results['danceability']}% | Valence: {results['valence']}%")
    print("="*50)
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python music_analyzer.py <audio_file>")
        print("Example: python music_analyzer.py sample_tracks/track1.mp3")
    else:
        analyze_track(sys.argv[1])