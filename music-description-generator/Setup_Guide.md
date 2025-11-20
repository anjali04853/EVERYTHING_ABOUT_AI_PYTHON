# Music Description Generator - Setup Guide

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Check version: `python --version` or `python3 --version`

2. **FFmpeg** (for audio processing)
   - **Windows**: Download from https://ffmpeg.org/download.html
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for dependencies
- **OS**: Windows 10/11, macOS 10.14+, or Linux

## 📦 Installation

### Step 1: Create Project Directory

```bash
# Create and navigate to project folder
mkdir music-description-generator
cd music-description-generator
```

### Step 2: Set Up Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Note**: This may take 5-10 minutes depending on your internet speed.

### Step 4: Create Project Structure

Create the following directory structure:

```
music-description-generator/
│
├── music_analyzer.py          # Main analysis engine
├── batch_analyzer.py          # Batch processing script
├── app.py                     # Flask web application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── templates/                 # HTML templates
│   └── index.html            # Web interface
│
├── uploads/                   # Temporary upload folder (auto-created)
├── sample_tracks/            # Your audio files for testing
├── analysis_results/         # Single file analysis output
└── batch_results/            # Batch analysis output
```

Create the necessary folders:
```bash
mkdir templates uploads sample_tracks analysis_results batch_results
```

### Step 5: Add Sample Audio Files

Place some audio files (MP3, WAV, FLAC) in the `sample_tracks/` folder for testing.

## 📁 Project Structure

```
music-description-generator/
│
├── Core Python Files
│   ├── music_analyzer.py        # Audio analysis engine with ML models
│   ├── batch_analyzer.py        # Batch processing for multiple files
│   └── app.py                   # Web server application
│
├── Web Interface
│   └── templates/
│       └── index.html          # Beautiful web UI
│
├── Configuration
│   ├── requirements.txt        # Python package dependencies
│   ├── README.md              # Project documentation
│   └── SETUP_GUIDE.md         # This file
│
├── Data Directories (auto-created)
│   ├── uploads/               # Temporary file storage
│   ├── sample_tracks/         # Test audio files
│   ├── analysis_results/      # Single file results
│   └── batch_results/         # Batch analysis results
│       ├── individual_tracks/ # Per-track analyses
│       ├── genre_reports/     # Genre-specific reports
│       ├── analysis_summary.txt
│       └── music_analysis.csv
```

## 🚀 Running the Application

### Method 1: Web Interface (Recommended)

Start the Flask web server:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Web Interface Features:**
- Drag & drop audio upload
- Real-time analysis visualization
- Multiple description format generation
- Copy to clipboard functionality
- Download descriptions as text files
- Beautiful, responsive design

### Method 2: Command Line - Single File Analysis

Analyze a single audio file:

```bash
python music_analyzer.py sample_tracks/your_song.mp3
```

**Output:**
- JSON file with complete analysis
- 4 text files (YouTube, Podcast, Library, Social Media descriptions)
- Console summary

### Method 3: Batch Processing

Analyze multiple files at once:

```bash
python batch_analyzer.py sample_tracks/
```

**Output:**
- Individual analysis for each track
- Comprehensive summary report
- CSV export for data analysis
- Genre-specific reports
- Statistics and insights

### Method 4: Custom Output Directory

Specify custom output location:

```bash
# Single file
python music_analyzer.py song.mp3 custom_output/

# Batch processing
python batch_analyzer.py input_folder/ custom_output/
```

## 💡 Usage Examples

### Example 1: Analyze Your Music Library

```bash
# Copy your music files
cp ~/Music/*.mp3 sample_tracks/

# Run batch analysis
python batch_analyzer.py sample_tracks/ my_library_analysis/
```

### Example 2: Generate YouTube Descriptions

```bash
# Analyze track
python music_analyzer.py sample_tracks/song.mp3

# Check the _youtube.txt file in analysis_results/
cat analysis_results/song_youtube.txt
```

### Example 3: Use Web Interface for Quick Analysis

```bash
# Start server
python app.py

# Open browser to http://localhost:5000
# Drag & drop your audio file
# Select format (YouTube, Podcast, etc.)
# Click "Copy to Clipboard"
```

### Example 4: Export to Spreadsheet

```bash
# Analyze tracks
python batch_analyzer.py sample_tracks/

# Open the CSV file
# Located at: batch_results/music_analysis.csv
# Import into Excel, Google Sheets, etc.
```

## 🎯 Features Explained

### Audio Analysis Features

1. **Genre Classification**
   - Primary genre detection
   - Sub-genre identification
   - Based on spectral features

2. **Mood Detection**
   - Energy level analysis
   - Emotional valence calculation
   - Tonality assessment

3. **Musical Properties**
   - Tempo (BPM) detection
   - Key and mode identification
   - Time signature estimation

4. **Instrument Recognition**
   - Spectral-based detection
   - Frequency range analysis
   - Up to 5 instruments identified

5. **Audio Features (Spotify-style)**
   - Energy (0-100%)
   - Danceability (0-100%)
   - Valence/Positivity (0-100%)
   - Loudness (dB)

### Description Formats

1. **YouTube**
   - Complete track information
   - Technical specifications
   - Use case suggestions
   - Hashtags included

2. **Podcast**
   - Podcast-specific recommendations
   - Segment usage suggestions
   - Background music description

3. **Music Library**
   - Metadata tags
   - Complete technical specs
   - Searchable keywords

4. **Social Media**
   - Short, engaging format
   - Hashtags optimized
   - Platform-ready content

## 🔍 Understanding the Output

### Analysis JSON Structure

```json
{
  "file_name": "song.mp3",
  "duration": "3:45",
  "tempo": 128.5,
  "key": "C Major",
  "time_signature": "4/4",
  "genre": "Electronic",
  "sub_genre": "House",
  "mood": "Energetic & Uplifting",
  "instruments": ["Synthesizer", "Bass", "Drums"],
  "energy": 85,
  "danceability": 78,
  "valence": 72,
  "loudness": -6.5,
  "analysis_date": "2024-01-15 14:30:00"
}
```

### Batch Analysis Reports

**Summary Report** (`analysis_summary.txt`):
- Genre distribution
- Mood statistics
- Tempo analysis
- Energy levels
- Top tracks by feature

**CSV Export** (`music_analysis.csv`):
- All tracks in tabular format
- Easy filtering and sorting
- Import into spreadsheet software

**Genre Reports** (`genre_reports/`):
- Separate report per genre
- Sub-genre breakdown
- Average characteristics
- Track listings

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "No module named 'librosa'"
**Problem**: Dependencies not installed
**Solution**:
```bash
pip install -r requirements.txt
```

#### 2. "FFmpeg not found"
**Problem**: FFmpeg not in system PATH
**Solution**:
- **Windows**: Add FFmpeg to PATH or reinstall
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

#### 3. "Could not load audio file"
**Problem**: Unsupported audio format or corrupted file
**Solution**:
- Convert to MP3 or WAV format
- Verify file is not corrupted
- Check file permissions

#### 4. "Memory Error"
**Problem**: Large file exceeds available RAM
**Solution**:
- Use shorter audio clips (first 60 seconds analyzed by default)
- Close other applications
- Upgrade RAM if possible

#### 5. Web Server Won't Start
**Problem**: Port 5000 already in use
**Solution**:
```bash
# Use different port
flask run --port 5001
```

#### 6. Slow Analysis
**Problem**: Large files or slow CPU
**Solution**:
- Analyses first 60 seconds by default
- Close background applications
- Use batch mode for multiple files (more efficient)

### Performance Tips

1. **Use Batch Mode**: More efficient for multiple files
2. **Optimize File Size**: Convert to lower bitrate if needed
3. **Close Applications**: Free up system resources
4. **Use SSD**: Faster file I/O operations

## 📊 Sample Output Examples

### Console Output

```
Analyzing: epic_track.mp3
--------------------------------------------------
Loading Hugging Face models...
Music Analyzer initialized successfully!

==================================================
ANALYSIS SUMMARY
==================================================
File: epic_track.mp3
Genre: Electronic - House
Mood: Energetic & Uplifting
Tempo: 128.0 BPM | Key: C Major
Duration: 3:45
Instruments: Synthesizer, Bass, Drums, Hi-Hat/Cymbals

Energy: 85% | Danceability: 78% | Valence: 72%
==================================================

✓ Saved analysis: analysis_results/epic_track_analysis.json
✓ Saved youtube description: analysis_results/epic_track_youtube.txt
✓ Saved podcast description: analysis_results/epic_track_podcast.txt
✓ Saved library description: analysis_results/epic_track_library.txt
✓ Saved social description: analysis_results/epic_track_social.txt
```

### Batch Analysis Summary

```
======================================================================
MUSIC LIBRARY ANALYSIS REPORT
======================================================================
Generated: 2024-01-15 14:30:00
Total Tracks Analyzed: 25

GENRE DISTRIBUTION
----------------------------------------------------------------------
  Electronic: 10 tracks (40.0%)
  Hip Hop: 6 tracks (24.0%)
  Pop: 5 tracks (20.0%)
  R&B: 4 tracks (16.0%)

MOOD DISTRIBUTION
----------------------------------------------------------------------
  Energetic & Uplifting: 12 tracks (48.0%)
  Peaceful & Calm: 8 tracks (32.0%)
  Intense & Driving: 5 tracks (20.0%)

TEMPO ANALYSIS
----------------------------------------------------------------------
  Average Tempo: 122.5 BPM
  Fastest Track: 145.0 BPM
  Slowest Track: 85.0 BPM
```

## 🔄 Updating the System

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To update specific packages:

```bash
pip install --upgrade librosa transformers
```

## 📝 Configuration Options

### Modify Analysis Duration

In `music_analyzer.py`, line 38:
```python
y, sr = librosa.load(audio_path, duration=60)  # Change 60 to desired seconds
```

### Change Web Server Port

In `app.py`, last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port number
```

### Adjust File Size Limit

In `app.py`, line 12:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Change 50 to desired MB
```

## 🎓 Learning Resources

- **Librosa Documentation**: https://librosa.org/doc/latest/
- **Hugging Face Audio**: https://huggingface.co/docs/transformers/tasks/audio_classification
- **Music Information Retrieval**: https://www.audiocontentanalysis.org/

## 📧 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed
3. Check Python version compatibility
4. Review error messages carefully

## 🎉 You're All Set!

Start analyzing music:
```bash
# Start web interface
python app.py

# Or analyze from command line
python music_analyzer.py sample_tracks/your_song.mp3
```

Enjoy generating professional music descriptions! 🎵